# AxiomHive Commercial Purchase Flow

## Overview

AxiomHive offers commercial software licenses for individuals, businesses, and enterprises. All purchases are conducted via Bitcoin payments to ensure privacy, security, and sovereignty. This document outlines the complete purchase and activation process.

## License Types

### Personal License ($50 USD / 0.001 BTC)
- **Use Case**: Individual personal projects
- **Features**:
  - Core cognitive modules
  - Personal use only
  - 3 hardware activations
  - 1 year validity
- **Price**: 0.001 BTC (100,000 sats)

### Commercial License ($250 USD / 0.005 BTC)
- **Use Case**: Business applications
- **Features**:
  - Commercial use permitted
  - Advanced cognitive modules
  - Priority support
  - 10 hardware activations
  - 1 year validity
- **Price**: 0.005 BTC (500,000 sats)

### Enterprise License ($500 USD / 0.01 BTC)
- **Use Case**: Large organizations
- **Features**:
  - All cognitive modules
  - Enterprise support
  - Custom integration options
  - API access
  - 100 hardware activations
  - 3 year validity
- **Price**: 0.01 BTC (1,000,000 sats)

## Purchase Process

### Step 1: Initiate Purchase

Visit `https://axiomhive.co/purchase` and select your license type.

**API Endpoint**: `POST /api/commercial/purchase/initiate`

```json
{
  "customer_email": "user@example.com",
  "license_type": "personal"
}
```

**Response**:
```json
{
  "order": {
    "order_id": "ORDER-ABC123XYZ",
    "customer_email": "user@example.com",
    "license_type": "personal",
    "payment_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "expected_amount_btc": 0.001,
    "pricing": {
      "price_btc": 0.001,
      "price_usd": 50,
      "features": ["Personal use", "3 activations", "1 year support"],
      "description": "Individual use license for personal projects"
    }
  },
  "payment_instructions": "Bitcoin Payment Instructions for AxiomHive License...",
  "download_links": {
    "direct_download": "https://axiomhive.co/download",
    "github_releases": "https://github.com/AXI0MH1VE/AxiomHive-LexLab/releases"
  }
}
```

### Step 2: Make Bitcoin Payment

Send the exact amount of Bitcoin to the provided payment address:

- **Payment Address**: `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh`
- **Amount**: As specified in your order (0.001 BTC for personal license)
- **Important**: Include a small miner fee for faster confirmation

**Payment Instructions**:
```
Bitcoin Payment Instructions for AxiomHive License

Order ID: ORDER-ABC123XYZ
Amount: 0.001 BTC (50 USD)
Payment Address: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

Steps:
1. Copy the payment address above
2. Send exactly 0.001 BTC to this address
3. Wait for 1 confirmation (about 10 minutes)
4. Note your transaction hash (TXID)
5. Return to axiomhive.co/activate with your TXID to complete activation
```

### Step 3: Verify Payment and Generate License

After payment confirmation (1 Bitcoin confirmation), submit your transaction details:

**API Endpoint**: `POST /api/commercial/purchase/complete`

```json
{
  "order_id": "ORDER-ABC123XYZ",
  "tx_hash": "a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890",
  "amount_btc": 0.001,
  "sender_address": "bc1q[your-wallet-address]"
}
```

**Response**:
```json
{
  "success": true,
  "order": {
    "order_id": "ORDER-ABC123XYZ",
    "status": "completed",
    "license_id": "AXH-A1B2C3D4E5F6",
    "completed_at": "2025-10-06T09:45:30.000Z"
  },
  "license": {
    "license_id": "AXH-A1B2C3D4E5F6",
    "customer_email": "user@example.com",
    "license_type": "personal",
    "activation_key": "A1B2C3D4E5F67890",
    "expires_at": "2026-10-06T09:45:30.000Z",
    "max_activations": 3,
    "features": ["core_cognitive_modules", "personal_use_only"]
  },
  "activation_instructions": "AxiomHive License Activation Instructions..."
}
```

### Step 4: Download and Install

Download AxiomHive from the provided links and install on your system.

### Step 5: Activate License

Use the license activation command:

```bash
axiomhive activate --license-id AXH-A1B2C3D4E5F6 --activation-key A1B2C3D4E5F67890
```

**API Endpoint**: `POST /api/commercial/license/activate`

```json
{
  "license_id": "AXH-A1B2C3D4E5F6",
  "hardware_id": "HWID-1234567890",
  "installation_path": "/opt/axiomhive"
}
```

**Response**:
```json
{
  "success": true,
  "license_data": {
    "license_id": "AXH-A1B2C3D4E5F6",
    "status": "active",
    "activations": [
      {
        "hardware_id": "HWID-1234567890",
        "installation_path": "/opt/axiomhive",
        "activated_at": "2025-10-06T09:45:30.000Z"
      }
    ]
  }
}
```

## License Management

### Check License Status

**API Endpoint**: `POST /api/commercial/license/validate`

```json
{
  "license_id": "AXH-A1B2C3D4E5F6",
  "hardware_id": "HWID-1234567890"
}
```

### Transfer License

Contact support@axiomhive.co for license transfers between hardware.

### Renew License

Purchase renewal before expiration date.

## Support

- **Email**: support@axiomhive.co
- **Documentation**: https://docs.axiomhive.co
- **Community**: https://forum.axiomhive.co

## Refund Policy

- Refunds available within 30 days of purchase
- Must include original transaction details
- Processing time: 7-14 days
- Contact: refunds@axiomhive.co

## Security

- All payments verified on Bitcoin blockchain
- License keys cryptographically signed
- Hardware binding prevents unauthorized use
- No personal data stored without consent

## Bitcoin Payment Details

- **Network**: Bitcoin mainnet
- **Address Format**: Bech32 (bc1...)
- **Confirmations Required**: 1
- **Payment Window**: 24 hours
- **Currency**: BTC only (no altcoins accepted)

For questions about Bitcoin payments, visit: https://bitcoin.org/en/getting-started