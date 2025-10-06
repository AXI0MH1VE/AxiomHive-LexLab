import neo4j
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import hashlib
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryTraceManager:
    """
    Graph-based memory management system for historical context and proactive memory utilization.
    Manages conversation traces, user interactions, and semantic relationships in a Neo4j graph database.
    """

    def __init__(self, uri="bolt://neo4j:7687", user="neo4j", password="password"):
        logger.info("Initializing Memory Trace Manager. Connecting to graph database.")
        try:
            self.driver = neo4j.GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j.")
        except Exception as e:
            logger.error(f"Could not connect to Neo4j: {e}. Memory functions will be disabled.")
            self.driver = None

        # Proactive memory cache for frequently accessed memories
        self.memory_cache = {}
        self.cache_expiry = timedelta(hours=1)
        self.max_cache_size = 1000

    def close(self):
        if self.driver:
            self.driver.close()

    def _get_cache_key(self, user_id: str, content: str) -> str:
        """Generate cache key for memory entries"""
        return hashlib.md5(f"{user_id}:{content}".encode()).hexdigest()

    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        return datetime.now() - cache_entry['timestamp'] < self.cache_expiry

    def _manage_cache_size(self):
        """Proactively manage cache size by removing expired entries"""
        current_time = datetime.now()
        valid_entries = {
            k: v for k, v in self.memory_cache.items()
            if current_time - v['timestamp'] < self.cache_expiry
        }
        self.memory_cache = valid_entries

        # If still too large, remove oldest entries
        if len(self.memory_cache) > self.max_cache_size:
            sorted_entries = sorted(self.memory_cache.items(), key=lambda x: x[1]['timestamp'])
            self.memory_cache = dict(sorted_entries[-self.max_cache_size:])

    def store_interaction(self, user_id: str, user_message: str, assistant_response: str):
        """
        Store a conversation interaction in the graph database.
        Creates nodes for user, message, and response with semantic relationships.
        """
        if not self.driver:
            logger.warning("Neo4j not available, interaction not stored.")
            return

        timestamp = datetime.now().isoformat()
        interaction_id = f"{user_id}_{int(datetime.now().timestamp())}"

        with self.driver.session() as session:
            # Create user node if not exists
            session.run("""
                MERGE (u:User {id: $user_id})
                SET u.last_interaction = $timestamp
                """, user_id=user_id, timestamp=timestamp)

            # Create interaction node
            session.run("""
                CREATE (i:Interaction {
                    id: $interaction_id,
                    user_message: $user_message,
                    assistant_response: $assistant_response,
                    timestamp: $timestamp,
                    user_id: $user_id
                })
                """, interaction_id=interaction_id, user_message=user_message,
                assistant_response=assistant_response, timestamp=timestamp, user_id=user_id)

            # Link user to interaction
            session.run("""
                MATCH (u:User {id: $user_id})
                MATCH (i:Interaction {id: $interaction_id})
                CREATE (u)-[:HAS_INTERACTION]->(i)
                """, user_id=user_id, interaction_id=interaction_id)

            # Extract and link concepts from messages
            user_concepts = self._extract_concepts(user_message)
            response_concepts = self._extract_concepts(assistant_response)

            for concept in user_concepts:
                session.run("""
                    MERGE (c:Concept {name: $concept})
                    MATCH (i:Interaction {id: $interaction_id})
                    CREATE (i)-[:MENTIONS {source: 'user'}]->(c)
                    """, concept=concept, interaction_id=interaction_id)

            for concept in response_concepts:
                session.run("""
                    MERGE (c:Concept {name: $concept})
                    MATCH (i:Interaction {id: $interaction_id})
                    CREATE (i)-[:MENTIONS {source: 'assistant'}]->(c)
                    """, concept=concept, interaction_id=interaction_id)

        # Update proactive cache
        cache_key = self._get_cache_key(user_id, user_message)
        self.memory_cache[cache_key] = {
            'response': assistant_response,
            'concepts': user_concepts + response_concepts,
            'timestamp': datetime.now()
        }
        self._manage_cache_size()

        logger.info(f"Interaction stored for user {user_id}: {len(user_message)} chars -> {len(assistant_response)} chars")

    def recall_relevant(self, user_id: str, current_message: str, limit: int = 5) -> Optional[Dict[str, Any]]:
        """
        Recall relevant historical context based on current message.
        Uses semantic similarity and graph relationships for proactive retrieval.
        """
        if not self.driver:
            # Fallback to cache-only recall
            cache_key = self._get_cache_key(user_id, current_message)
            if cache_key in self.memory_cache and self._is_cache_valid(self.memory_cache[cache_key]):
                return self.memory_cache[cache_key]
            return None

        # First check proactive cache
        cache_key = self._get_cache_key(user_id, current_message)
        if cache_key in self.memory_cache and self._is_cache_valid(self.memory_cache[cache_key]):
            logger.info(f"Cache hit for user {user_id}")
            return self.memory_cache[cache_key]

        # Extract concepts from current message
        current_concepts = self._extract_concepts(current_message)

        with self.driver.session() as session:
            # Find interactions with similar concepts
            if current_concepts:
                concept_list = ", ".join(f"'{c}'" for c in current_concepts)
                result = session.run(f"""
                    MATCH (u:User {{id: $user_id}})-[:HAS_INTERACTION]->(i:Interaction)-[:MENTIONS]->(c:Concept)
                    WHERE c.name IN [{concept_list}]
                    RETURN i.user_message as message, i.assistant_response as response,
                           i.timestamp as timestamp, count(c) as relevance_score
                    ORDER BY relevance_score DESC, i.timestamp DESC
                    LIMIT $limit
                    """, user_id=user_id, limit=limit)
            else:
                # Fallback to recent interactions
                result = session.run("""
                    MATCH (u:User {id: $user_id})-[:HAS_INTERACTION]->(i:Interaction)
                    RETURN i.user_message as message, i.assistant_response as response,
                           i.timestamp as timestamp, 1 as relevance_score
                    ORDER BY i.timestamp DESC
                    LIMIT $limit
                    """, user_id=user_id, limit=limit)

            records = list(result)
            if records:
                # Return most relevant interaction
                most_relevant = records[0]
                context = {
                    'message': most_relevant['message'],
                    'response': most_relevant['response'],
                    'timestamp': most_relevant['timestamp'],
                    'relevance_score': most_relevant['relevance_score'],
                    'related_interactions': len(records)
                }

                # Cache for future use
                self.memory_cache[cache_key] = {
                    'response': context['response'],
                    'concepts': current_concepts,
                    'timestamp': datetime.now(),
                    'context': context
                }
                self._manage_cache_size()

                return context

        return None

    def _extract_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts from text for semantic linking.
        Simple keyword extraction - could be enhanced with NLP.
        """
        # Basic concept extraction (can be enhanced with NLP models)
        words = text.lower().split()
        concepts = []

        # Filter for potential concepts (noun-like words, >3 chars)
        for word in words:
            word = word.strip('.,!?;:')
            if len(word) > 3 and word not in ['that', 'this', 'with', 'from', 'they', 'have', 'been', 'were', 'what', 'when', 'where', 'how', 'why', 'who']:
                concepts.append(word)

        return list(set(concepts))  # Remove duplicates

    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get comprehensive user context including interaction history and patterns.
        """
        if not self.driver:
            return {'interactions': 0, 'concepts': [], 'last_interaction': None}

        with self.driver.session() as session:
            # Get user stats
            user_result = session.run("""
                MATCH (u:User {id: $user_id})
                OPTIONAL MATCH (u)-[:HAS_INTERACTION]->(i:Interaction)
                RETURN u.last_interaction as last_interaction, count(i) as interaction_count
                """, user_id=user_id)

            user_data = user_result.single()
            if not user_data:
                return {'interactions': 0, 'concepts': [], 'last_interaction': None}

            # Get most common concepts
            concept_result = session.run("""
                MATCH (u:User {id: $user_id})-[:HAS_INTERACTION]->(i:Interaction)-[:MENTIONS]->(c:Concept)
                RETURN c.name as concept, count(c) as frequency
                ORDER BY frequency DESC
                LIMIT 10
                """, user_id=user_id)

            concepts = [{'name': r['concept'], 'frequency': r['frequency']} for r in concept_result]

            return {
                'interactions': user_data['interaction_count'],
                'concepts': concepts,
                'last_interaction': user_data['last_interaction']
            }

    def add_memory(self, concept: str, properties: dict):
        """Legacy method for backward compatibility"""
        if not self.driver: return
        with self.driver.session() as session:
            session.run("MERGE (c:Concept {name: $concept}) SET c += $properties",
                        concept=concept, properties=properties)
        logger.info(f"Memory added: Concept='{concept}'")

    def create_relationship(self, concept1: str, relationship: str, concept2: str):
        """Legacy method for backward compatibility"""
        if not self.driver: return
        with self.driver.session() as session:
            query = (
                "MATCH (a:Concept {name: $concept1}) "
                "MATCH (b:Concept {name: $concept2}) "
                "MERGE (a)-[r:%s]->(b)" % relationship.upper()
            )
            session.run(query, concept1=concept1, concept2=concept2)
        logger.info(f"Relationship created: {concept1} -> {relationship} -> {concept2}")

    def recall(self, concept: str) -> list:
        """Legacy method for backward compatibility"""
        if not self.driver: return []
        with self.driver.session() as session:
            result = session.run("MATCH (c:Concept {name: $concept})-[r]-(related) "
                                 "RETURN type(r) as relationship, related.name as related_concept",
                                 concept=concept)
            return [{"relationship": record["relationship"], "concept": record["related_concept"]} for record in result]
