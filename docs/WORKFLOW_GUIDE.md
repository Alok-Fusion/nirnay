# NIRNAY - Workflow & Demo Guide

## The Enterprise Hackathon Demo
We have crafted an interactive Demo Mode to showcase the Agentic Intelligence of the platform.

### How to Run
```bash
# Ensure virtual environment is active
python scripts/run_ai_scenario.py
```

### Supported Scenarios
1. **Normal Transfer:** A standard, low-risk transaction that gets automatically approved.
2. **Crypto Scam:** A high-value transfer to a crypto exchange triggered from a new device IP.
3. **Investment Scam:** A transfer to a known bad actor with a high scam count.
4. **Romance Scam:** Unusually high trust score but a zero transaction history.
5. **Fake Bank Officer:** Immediate wire transfer to a "safe account".
6. **Deepfake Scam:** "CEO Emergency Fund" request.
7. **Lottery Scam:** Small upfront fee transfer to "Global Winners".
8. **Emergency Relative Scam:** Bail money request.

### The Decision Trace Dashboard
Upon completion, the system outputs an enterprise-grade Decision Trace:

```
================================================
Decision Trace
================================================
Transaction         : TX-CRYPTO-4592
Amount              : USD 15000.0
Recipient           : Coinbase Exchange
Transfer Type       : TRANSFER
Risk Score          : 95.44
Confidence          : 90.87%
Reason Codes        : amount_deviation, new_recipient
Evidence            : The transaction has a critical risk score of 95.44...
Policy Applied      : Require Customer Confirmation
Customer Response   : Yes, I authorized this.
Recommendations     : Continue Transaction, Monitor Account, Review Safety Tips
Final Recommendation: End
Memory Used         : True
Workflow Status     : COMPLETED
```

### Performance Metrics
The system also outputs granular metrics tracking the execution time (in seconds) of every agent and the Total Workflow Time.
