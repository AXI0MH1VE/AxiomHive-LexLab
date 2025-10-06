"""
Commercial Licensing System for AxiomHive
Handles Bitcoin payments, license generation, and software activation
"""

import logging
import hashlib
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import base64
import secrets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BitcoinPaymentVerifier:
    """Verifies Bitcoin payments for license activation"""

    def __init__(self, expected_address: str = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"):
        self.expected_address = expected_address
        self.expected_amount_btc = 0.001  # 100,000 sats
        self.confirmation_threshold = 1  # Require 1 confirmation
        logger.info(f"Bitcoin Payment Verifier initialized for address: {expected_address}")

    def verify_payment(self, tx_hash: str, amount_btc: float, sender_address: str) -> Dict[str, Any]:
        """
        Verify Bitcoin payment details
        In production, this would query a Bitcoin node or API
        """
        verification = {
            'verified': False,
            'tx_hash': tx_hash,
            'amount_btc': amount_btc,
            'expected_amount': self.expected_amount_btc,
            'confirmations': 0,
            'timestamp': datetime.now().isoformat(),
            'error': None
        }

        # Basic validation
        if amount_btc < self.expected_amount_btc:
            verification['error'] = f"Insufficient amount: {amount_btc} BTC < {self.expected_amount_btc} BTC"
            return verification

        # In production, verify against blockchain
        # For demo purposes, we'll simulate verification
        if self._simulate_blockchain_check(tx_hash, amount_btc, sender_address):
            verification['verified'] = True
            verification['confirmations'] = self.confirmation_threshold + 1
            logger.info(f"Payment verified: {tx_hash}")
        else:
            verification['error'] = "Payment verification failed"

        return verification

    def _simulate_blockchain_check(self, tx_hash: str, amount: float, sender: str) -> bool:
        """Simulate blockchain verification (replace with real API calls)"""
        # This would normally query blockchain.info, blockcypher, or a Bitcoin node
        # For demo: accept any tx_hash that starts with valid characters
        return len(tx_hash) >= 64 and amount >= self.expected_amount_btc

class LicenseGenerator:
    """Generates and manages software licenses"""

    def __init__(self, private_key_path: Optional[str] = None):
        self.private_key_path = private_key_path or "license_keys/private.pem"
        self.licenses_db = {}
        self.load_existing_licenses()
        logger.info("License Generator initialized")

    def generate_license(self, customer_email: str, tx_hash: str,
                        license_type: str = "personal") -> Dict[str, Any]:
        """Generate a new software license"""

        license_id = self._generate_license_id()
        activation_key = self._generate_activation_key()

        license_data = {
            'license_id': license_id,
            'customer_email': customer_email,
            'tx_hash': tx_hash,
            'license_type': license_type,
            'activation_key': activation_key,
            'issued_at': datetime.now().isoformat(),
            'expires_at': self._calculate_expiry(license_type),
            'features': self._get_license_features(license_type),
            'max_activations': self._get_max_activations(license_type),
            'activations': [],
            'status': 'issued'
        }

        # Sign the license
        license_data['signature'] = self._sign_license(license_data)

        self.licenses_db[license_id] = license_data
        self._save_licenses()

        logger.info(f"License generated: {license_id} for {customer_email}")
        return license_data

    def activate_license(self, license_id: str, hardware_id: str,
                        installation_path: str) -> Dict[str, Any]:
        """Activate a license on a specific machine"""

        license_data = self.licenses_db.get(license_id)
        if not license_data:
            return {'success': False, 'error': 'License not found'}

        if license_data['status'] != 'issued':
            return {'success': False, 'error': 'License not eligible for activation'}

        # Check activation limits
        if len(license_data['activations']) >= license_data['max_activations']:
            return {'success': False, 'error': 'Maximum activations reached'}

        # Check if already activated on this hardware
        for activation in license_data['activations']:
            if activation['hardware_id'] == hardware_id:
                return {'success': False, 'error': 'Already activated on this hardware'}

        # Create activation record
        activation_record = {
            'hardware_id': hardware_id,
            'installation_path': installation_path,
            'activated_at': datetime.now().isoformat(),
            'last_check': datetime.now().isoformat()
        }

        license_data['activations'].append(activation_record)
        license_data['status'] = 'active'
        self._save_licenses()

        logger.info(f"License activated: {license_id} on hardware {hardware_id}")
        return {
            'success': True,
            'license_data': license_data,
            'activation_record': activation_record
        }

    def validate_license(self, license_id: str, hardware_id: str) -> Dict[str, Any]:
        """Validate an active license"""

        license_data = self.licenses_db.get(license_id)
        if not license_data:
            return {'valid': False, 'error': 'License not found'}

        # Check expiry
        if datetime.now() > datetime.fromisoformat(license_data['expires_at']):
            return {'valid': False, 'error': 'License expired'}

        # Check if activated on this hardware
        activation_found = False
        for activation in license_data['activations']:
            if activation['hardware_id'] == hardware_id:
                activation_found = True
                activation['last_check'] = datetime.now().isoformat()
                break

        if not activation_found:
            return {'valid': False, 'error': 'Not activated on this hardware'}

        self._save_licenses()
        return {
            'valid': True,
            'license_data': license_data,
            'features': license_data['features']
        }

    def _generate_license_id(self) -> str:
        """Generate unique license ID"""
        return f"AXH-{secrets.token_hex(8).upper()}"

    def _generate_activation_key(self) -> str:
        """Generate activation key"""
        return secrets.token_hex(16).upper()

    def _calculate_expiry(self, license_type: str) -> str:
        """Calculate license expiry date"""
        if license_type == 'personal':
            expiry = datetime.now() + timedelta(days=365)
        elif license_type == 'commercial':
            expiry = datetime.now() + timedelta(days=365)
        elif license_type == 'enterprise':
            expiry = datetime.now() + timedelta(days=365*3)
        else:
            expiry = datetime.now() + timedelta(days=365)

        return expiry.isoformat()

    def _get_license_features(self, license_type: str) -> List[str]:
        """Get features for license type"""
        base_features = [
            'core_cognitive_modules',
            'basic_reasoning',
            'memory_trace',
            'ethics_sentinel'
        ]

        if license_type == 'personal':
            return base_features + ['personal_use_only']
        elif license_type == 'commercial':
            return base_features + [
                'commercial_use',
                'priority_support',
                'advanced_modules'
            ]
        elif license_type == 'enterprise':
            return base_features + [
                'commercial_use',
                'enterprise_support',
                'all_modules',
                'custom_integration',
                'api_access'
            ]
        else:
            return base_features

    def _get_max_activations(self, license_type: str) -> int:
        """Get maximum activations for license type"""
        limits = {
            'personal': 3,      # Home computer + laptop + backup
            'commercial': 10,   # Small team
            'enterprise': 100   # Large organization
        }
        return limits.get(license_type, 3)

    def _sign_license(self, license_data: Dict[str, Any]) -> str:
        """Sign license data (simplified for demo)"""
        # In production, use proper cryptographic signing
        data_str = json.dumps(license_data, sort_keys=True)
        signature = hashlib.sha256(data_str.encode()).hexdigest()
        return signature

    def load_existing_licenses(self):
        """Load existing licenses from storage"""
        try:
            license_file = Path("licenses/licenses.json")
            if license_file.exists():
                with open(license_file, 'r') as f:
                    self.licenses_db = json.load(f)
                logger.info(f"Loaded {len(self.licenses_db)} existing licenses")
        except Exception as e:
            logger.warning(f"Could not load existing licenses: {e}")
            self.licenses_db = {}

    def _save_licenses(self):
        """Save licenses to storage"""
        try:
            license_file = Path("licenses/licenses.json")
            license_file.parent.mkdir(exist_ok=True)
            with open(license_file, 'w') as f:
                json.dump(self.licenses_db, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save licenses: {e}")

class CommercialLicenseManager:
    """Main commercial licensing system orchestrator"""

    def __init__(self, bitcoin_address: str = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"):
        self.payment_verifier = BitcoinPaymentVerifier(bitcoin_address)
        self.license_generator = LicenseGenerator()
        self.pending_orders = {}
        logger.info("Commercial License Manager initialized")

    def create_purchase_order(self, customer_email: str, license_type: str = "personal") -> Dict[str, Any]:
        """Create a purchase order for Bitcoin payment"""

        order_id = f"ORDER-{secrets.token_hex(8).upper()}"
        payment_address = self.payment_verifier.expected_address
        expected_amount = self.payment_verifier.expected_amount_btc

        order = {
            'order_id': order_id,
            'customer_email': customer_email,
            'license_type': license_type,
            'payment_address': payment_address,
            'expected_amount_btc': expected_amount,
            'status': 'pending_payment',
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
        }

        self.pending_orders[order_id] = order

        logger.info(f"Purchase order created: {order_id} for {customer_email}")
        return order

    def process_payment_and_generate_license(self, order_id: str, tx_hash: str,
                                           amount_btc: float, sender_address: str) -> Dict[str, Any]:
        """Process Bitcoin payment and generate license"""

        order = self.pending_orders.get(order_id)
        if not order:
            return {'success': False, 'error': 'Order not found'}

        if order['status'] != 'pending_payment':
            return {'success': False, 'error': 'Order not eligible for payment processing'}

        # Verify payment
        payment_verification = self.payment_verifier.verify_payment(tx_hash, amount_btc, sender_address)

        if not payment_verification['verified']:
            return {
                'success': False,
                'error': payment_verification.get('error', 'Payment verification failed'),
                'payment_details': payment_verification
            }

        # Generate license
        license_data = self.license_generator.generate_license(
            customer_email=order['customer_email'],
            tx_hash=tx_hash,
            license_type=order['license_type']
        )

        # Update order status
        order['status'] = 'completed'
        order['license_id'] = license_data['license_id']
        order['completed_at'] = datetime.now().isoformat()
        order['payment_verification'] = payment_verification

        logger.info(f"Order completed: {order_id} -> License {license_data['license_id']}")
        return {
            'success': True,
            'order': order,
            'license': license_data,
            'activation_instructions': self._get_activation_instructions(license_data)
        }

    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get order status"""
        order = self.pending_orders.get(order_id)
        if not order:
            return {'error': 'Order not found'}

        return order

    def _get_activation_instructions(self, license_data: Dict[str, Any]) -> str:
        """Generate activation instructions for customer"""
        return f"""
AxiomHive License Activation Instructions

License ID: {license_data['license_id']}
Activation Key: {license_data['activation_key']}

To activate your license:

1. Download AxiomHive from: https://axiomhive.co/download
2. Install the software on your system
3. Run the activation command:
   axiomhive activate --license-id {license_data['license_id']} --activation-key {license_data['activation_key']}

Your license expires on: {license_data['expires_at']}
Maximum activations: {license_data['max_activations']}

For support: support@axiomhive.co
"""

class DistributionManager:
    """Manages software distribution and updates"""

    def __init__(self):
        self.distribution_channels = {
            'direct_download': 'https://axiomhive.co/download',
            'github_releases': 'https://github.com/AXI0MH1VE/AxiomHive-LexLab/releases',
            'torrent': 'https://axiomhive.co/torrent'
        }
        self.version_info = self._load_version_info()
        logger.info("Distribution Manager initialized")

    def get_download_links(self, license_type: str = "personal") -> Dict[str, str]:
        """Get download links based on license type"""
        base_links = self.distribution_channels.copy()

        # Add license-specific links if needed
        if license_type == "enterprise":
            base_links['enterprise_portal'] = 'https://enterprise.axiomhive.co'

        return base_links

    def check_for_updates(self, current_version: str) -> Dict[str, Any]:
        """Check for software updates"""
        latest_version = self.version_info.get('latest_version', current_version)

        if latest_version != current_version:
            return {
                'update_available': True,
                'latest_version': latest_version,
                'download_url': self.distribution_channels['direct_download'],
                'changelog': self.version_info.get('changelog', [])
            }
        else:
            return {'update_available': False}

    def _load_version_info(self) -> Dict[str, Any]:
        """Load version information"""
        # In production, this would fetch from a version API
        return {
            'latest_version': '1.0.0',
            'changelog': [
                'Complete cognitive backend implementation',
                'Commercial licensing system',
                'Bitcoin payment integration',
                'Advanced safety and ethics modules'
            ]
        }

class CommercialMonetizationService:
    """Main orchestrator for commercial monetization services"""

    def __init__(self, bitcoin_address: str = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"):
        logger.info("Commercial Monetization Service initialized")
        self.license_manager = CommercialLicenseManager(bitcoin_address)
        self.distribution_manager = DistributionManager()
        self.pricing = self._load_pricing()

    def initiate_purchase(self, customer_email: str, license_type: str = "personal") -> Dict[str, Any]:
        """Initiate a commercial purchase"""

        # Validate license type
        if license_type not in self.pricing:
            return {'error': f'Invalid license type: {license_type}'}

        # Create purchase order
        order = self.license_manager.create_purchase_order(customer_email, license_type)

        # Add pricing information
        order['pricing'] = self.pricing[license_type]

        return {
            'order': order,
            'payment_instructions': self._get_payment_instructions(order),
            'download_links': self.distribution_manager.get_download_links(license_type)
        }

    def complete_purchase(self, order_id: str, tx_hash: str, amount_btc: float, sender_address: str) -> Dict[str, Any]:
        """Complete purchase with payment verification"""
        return self.license_manager.process_payment_and_generate_license(
            order_id, tx_hash, amount_btc, sender_address
        )

    def validate_license(self, license_id: str, hardware_id: str) -> Dict[str, Any]:
        """Validate license activation"""
        return self.license_manager.license_generator.validate_license(license_id, hardware_id)

    def activate_license(self, license_id: str, hardware_id: str, installation_path: str) -> Dict[str, Any]:
        """Activate license on hardware"""
        return self.license_manager.license_generator.activate_license(license_id, hardware_id, installation_path)

    def _load_pricing(self) -> Dict[str, Dict[str, Any]]:
        """Load pricing information"""
        return {
            'personal': {
                'price_btc': 0.001,  # 100,000 sats
                'price_usd': 50,
                'features': ['Personal use', '3 activations', '1 year support'],
                'description': 'Individual use license for personal projects'
            },
            'commercial': {
                'price_btc': 0.005,  # 500,000 sats
                'price_usd': 250,
                'features': ['Commercial use', '10 activations', 'Priority support', 'Advanced modules'],
                'description': 'Business use license for commercial applications'
            },
            'enterprise': {
                'price_btc': 0.01,   # 1,000,000 sats
                'price_usd': 500,
                'features': ['Enterprise use', '100 activations', 'Premium support', 'All modules', 'API access'],
                'description': 'Enterprise license for large organizations'
            }
        }

    def _get_payment_instructions(self, order: Dict[str, Any]) -> str:
        """Generate payment instructions"""
        return f"""
Bitcoin Payment Instructions for AxiomHive License

Order ID: {order['order_id']}
Amount: {order['expected_amount_btc']} BTC ({order['pricing']['price_usd']} USD)
Payment Address: {order['payment_address']}

Steps:
1. Copy the payment address above
2. Send exactly {order['expected_amount_btc']} BTC to this address
3. Wait for 1 confirmation (about 10 minutes)
4. Note your transaction hash (TXID)
5. Return to axiomhive.co/activate with your TXID to complete activation

Important:
- Send from a wallet you control
- Include a small miner fee for faster confirmation
- Keep your TXID safe - you'll need it for activation

For support: payments@axiomhive.co
"""