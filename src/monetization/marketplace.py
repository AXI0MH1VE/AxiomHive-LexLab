import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DigitalMarketplace:
    """Agora Supremacy Engine Marketplace for AI services and tasks."""

    def __init__(self):
        logger.info("Initializing Digital Marketplace for Agora Supremacy Engine.")
        self._tasks = {}
        self._users = {}
        self._categories = set()
        self._completed_tasks = []

    def register_user(self, user_id: str, user_type: str = "agent"):
        """Register a new user (agent or client)."""
        if user_id in self._users:
            logger.warning(f"User {user_id} already registered.")
            return
        self._users[user_id] = {
            'type': user_type,
            'balance': 0.0,
            'reputation': 0.0,
            'completed_tasks': 0,
            'posted_tasks': 0
        }
        logger.info(f"Registered {user_type}: {user_id}")

    def post_task(self, task_id: str, client_id_or_description: str, description_or_prize,
                  prize: Optional[float] = None, category: str = "general",
                  deadline: Optional[datetime] = None):
        """Post a new task for bidding."""
        # Backward compatibility: old signature was (task_id, description, prize)
        if prize is None:
            # Old call: post_task('t', 'd', 1.0) -> task_id='t', description='d', prize=1.0
            client_id = "anonymous_client"
            description = client_id_or_description
            prize = float(description_or_prize)
        else:
            # New call: post_task(task_id, client_id, description, prize, ...)
            client_id = client_id_or_description
            description = description_or_prize

        if client_id not in self._users:
            self.register_user(client_id, "client")

        if deadline is None:
            deadline = datetime.now() + timedelta(days=7)

        self._tasks[task_id] = {
            'client_id': client_id,
            'description': description,
            'prize': prize,
            'category': category,
            'bids': [],
            'status': 'open',
            'posted_at': datetime.now(),
            'deadline': deadline
        }
        self._categories.add(category)
        self._users[client_id]['posted_tasks'] += 1
        logger.info(f"Task posted: {task_id} by {client_id}, prize: {prize}")

    def place_bid(self, task_id: str, agent_id: str, amount: float, proposal: str = ""):
        """Place a bid on a task."""
        if agent_id not in self._users:
            self.register_user(agent_id, "agent")

        task = self._tasks.get(task_id)
        if not task or task['status'] != 'open':
            logger.warning(f"Cannot bid on task {task_id}: not open or doesn't exist.")
            return False


        task['bids'].append({
            'agent_id': agent_id,
            'amount': amount,
            'proposal': proposal,
            'bid_time': datetime.now()
        })
        logger.info(f"Bid placed: {agent_id} on {task_id} for {amount}")
        return True

    def close_auction(self, task_id: str) -> Dict[str, Any]:
        """Close auction and select winner."""
        task = self._tasks.get(task_id)
        if not task or task['status'] != 'open':
            return {'agent_id': None, 'amount': 0, 'error': 'Task not open'}

        if not task['bids']:
            task['status'] = 'cancelled'
            return {'agent_id': None, 'amount': 0, 'error': 'No bids'}

        # Select lowest bid (reverse auction style)
        best_bid = min(task['bids'], key=lambda b: b['amount'])
        winner = best_bid['agent_id']

        task['status'] = 'awarded'
        task['winner'] = winner
        task['final_amount'] = best_bid['amount']

        # Update reputations
        self._users[winner]['reputation'] += 0.1
        self._users[task['client_id']]['reputation'] += 0.05

        logger.info(f"Auction closed: {task_id} awarded to {winner} for {best_bid['amount']}")
        return {
            'agent_id': winner,
            'amount': best_bid['amount'],
            'proposal': best_bid.get('proposal', '')
        }

    def complete_task(self, task_id: str, rating: float = 5.0):
        """Mark task as completed and update metrics."""
        task = self._tasks.get(task_id)
        if not task or task['status'] != 'awarded':
            return False

        task['status'] = 'completed'
        task['completed_at'] = datetime.now()
        task['rating'] = rating

        winner = task['winner']
        self._users[winner]['completed_tasks'] += 1
        self._users[winner]['reputation'] += rating * 0.1
        self._users[task['client_id']]['reputation'] += 0.1

        self._completed_tasks.append(task)
        logger.info(f"Task completed: {task_id}")
        return True

    def get_tasks_by_category(self, category: str) -> List[Dict]:
        """Get all open tasks in a category."""
        return [t for t in self._tasks.values() if t['category'] == category and t['status'] == 'open']

    def get_user_stats(self, user_id: str) -> Dict:
        """Get user statistics."""
        return self._users.get(user_id, {})

class ValueAssessor:
    """Assesses the value of AI services and tasks."""

    def __init__(self):
        logger.info("Value Assessor initialized for service valuation.")
        self.complexity_multipliers = {
            'simple': 1.0,
            'moderate': 1.5,
            'complex': 2.0,
            'expert': 3.0
        }
        self.category_base_rates = {
            'data_analysis': 50.0,
            'content_generation': 30.0,
            'code_development': 80.0,
            'research': 60.0,
            'consulting': 100.0,
            'general': 25.0
        }

    def assess_task_value(self, description: str, category: str = "general",
                         complexity: str = "moderate", urgency: str = "normal") -> float:
        """Assess the market value of a task."""
        base_rate = self.category_base_rates.get(category, self.category_base_rates['general'])
        complexity_mult = self.complexity_multipliers.get(complexity, 1.0)

        # Urgency multiplier
        urgency_mult = 1.0
        if urgency == "high":
            urgency_mult = 1.3
        elif urgency == "critical":
            urgency_mult = 1.6

        # Description length as proxy for scope
        scope_mult = min(1.0 + len(description.split()) / 100.0, 2.0)

        value = base_rate * complexity_mult * urgency_mult * scope_mult
        logger.info(f"Task value assessed: ${value:.2f} for {category}/{complexity}")
        return round(value, 2)

    def assess_service_value(self, service_type: str, quality_score: float = 1.0,
                           demand_factor: float = 1.0) -> float:
        """Assess ongoing service value."""
        base_value = self.category_base_rates.get(service_type, 25.0)
        value = base_value * quality_score * demand_factor
        return round(value, 2)

class PricingEngine:
    """Dynamic pricing engine for marketplace services."""

    def __init__(self):
        logger.info("Pricing Engine initialized for dynamic pricing.")
        self.market_rates = {}
        self.demand_history = []

    def calculate_dynamic_price(self, base_price: float, demand: float,
                              supply: float, competition: int) -> float:
        """Calculate dynamic price based on market conditions."""
        demand_mult = 1.0 + (demand - supply) * 0.1
        competition_mult = 1.0 - (competition * 0.05)

        price = base_price * demand_mult * competition_mult
        return max(price, base_price * 0.5)  # Floor at 50% of base

    def update_market_rates(self, category: str, transaction_price: float):
        """Update market rates based on completed transactions."""
        if category not in self.market_rates:
            self.market_rates[category] = []
        self.market_rates[category].append(transaction_price)
        # Keep last 100 transactions
        if len(self.market_rates[category]) > 100:
            self.market_rates[category].pop(0)

    def get_average_rate(self, category: str) -> float:
        """Get average market rate for category."""
        rates = self.market_rates.get(category, [])
        return sum(rates) / len(rates) if rates else 25.0

class TransactionManager:
    """Manages transactions and payments in the marketplace."""

    def __init__(self):
        logger.info("Transaction Manager initialized.")
        self.transactions = []
        self.escrow_accounts = {}

    def initiate_transaction(self, transaction_id: str, buyer_id: str, seller_id: str,
                           amount: float, task_id: str) -> bool:
        """Initiate a transaction with escrow."""
        if buyer_id not in self.escrow_accounts:
            self.escrow_accounts[buyer_id] = 0.0

        # Assume buyer has funds (in real system, check balance)
        if self.escrow_accounts.get(buyer_id, 0.0) < amount:
            logger.warning(f"Insufficient funds for {buyer_id}")
            return False

        self.escrow_accounts[buyer_id] -= amount
        self.transactions.append({
            'id': transaction_id,
            'buyer': buyer_id,
            'seller': seller_id,
            'amount': amount,
            'task_id': task_id,
            'status': 'escrow',
            'timestamp': datetime.now()
        })
        logger.info(f"Transaction initiated: {transaction_id} for ${amount}")
        return True

    def release_payment(self, transaction_id: str) -> bool:
        """Release payment from escrow to seller."""
        transaction = next((t for t in self.transactions if t['id'] == transaction_id), None)
        if not transaction or transaction['status'] != 'escrow':
            return False

        seller_id = transaction['seller']
        amount = transaction['amount']

        if seller_id not in self.escrow_accounts:
            self.escrow_accounts[seller_id] = 0.0
        self.escrow_accounts[seller_id] += amount

        transaction['status'] = 'completed'
        transaction['completed_at'] = datetime.now()
        logger.info(f"Payment released: {transaction_id}")
        return True

    def refund_transaction(self, transaction_id: str) -> bool:
        """Refund transaction to buyer."""
        transaction = next((t for t in self.transactions if t['id'] == transaction_id), None)
        if not transaction or transaction['status'] != 'escrow':
            return False

        buyer_id = transaction['buyer']
        amount = transaction['amount']

        self.escrow_accounts[buyer_id] += amount
        transaction['status'] = 'refunded'
        transaction['refunded_at'] = datetime.now()
        logger.info(f"Transaction refunded: {transaction_id}")
        return True

class MonetizationService:
    """Main orchestrator for monetization services in Agora Supremacy Engine."""

    def __init__(self):
        logger.info("Monetization Service initialized for Agora Supremacy Engine.")
        self.marketplace = DigitalMarketplace()
        self.value_assessor = ValueAssessor()
        self.pricing_engine = PricingEngine()
        self.transaction_manager = TransactionManager()

    def create_service_listing(self, service_id: str, provider_id: str, service_type: str,
                             description: str, base_price: float) -> bool:
        """Create a service listing for ongoing monetization."""
        assessed_value = self.value_assessor.assess_service_value(service_type)
        dynamic_price = self.pricing_engine.calculate_dynamic_price(
            base_price, demand=1.0, supply=1.0, competition=0
        )

        # Post as a persistent task/listing
        self.marketplace.post_task(
            task_id=f"service_{service_id}",
            client_id=provider_id,
            description=f"Service: {description}",
            prize=dynamic_price,
            category=service_type,
            deadline=None  # Ongoing service
        )
        logger.info(f"Service listing created: {service_id}")
        return True

    def process_transaction(self, task_id: str, winner_id: str, final_amount: float) -> bool:
        """Process a completed task transaction."""
        task = self.marketplace._tasks.get(task_id)
        if not task:
            return False

        transaction_id = f"txn_{task_id}_{winner_id}"
        success = self.transaction_manager.initiate_transaction(
            transaction_id=transaction_id,
            buyer_id=task['client_id'],
            seller_id=winner_id,
            amount=final_amount,
            task_id=task_id
        )

        if success:
            self.marketplace.complete_task(task_id)
            self.pricing_engine.update_market_rates(task['category'], final_amount)

        return success

    def get_market_analytics(self) -> Dict[str, Any]:
        """Get marketplace analytics."""
        total_tasks = len(self.marketplace._tasks)
        completed_tasks = len(self.marketplace._completed_tasks)
        total_volume = sum(t.get('final_amount', 0) for t in self.marketplace._completed_tasks)

        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completed_tasks / total_tasks if total_tasks > 0 else 0,
            'total_volume': total_volume,
            'categories': list(self.marketplace._categories),
            'active_users': len(self.marketplace._users)
        }
