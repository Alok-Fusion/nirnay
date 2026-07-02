# NIRNAY Authentication Guide

## Overview
Authentication is handled using JWT (JSON Web Tokens) and Argon2id for secure password hashing.

## Token Types
1. **Access Token:** Short-lived token (default 30 minutes) used to authorize API requests. Passed in the \Authorization\ header as a Bearer token.
2. **Refresh Token:** Long-lived token (default 7 days) used to obtain a new access token without requiring the user to log in again.

## Routes
- \POST /api/v1/auth/register\: Creates a new user. The password is hashed immediately using Argon2id before saving to the DB.
- \POST /api/v1/auth/login\: Accepts \username\ (email) and \password\ (OAuth2PasswordRequestForm standard). Returns the \ccess_token\ and \efresh_token\.

## Security Considerations
- **Argon2id:** Chosen over BCrypt as per security-first requirements to provide memory-hard hashing, protecting against GPU cracking.
- **Encryption:** Sensitive PII data in the DB (like recipient account numbers) is encrypted using \sqlalchemy-utils\ \EncryptedType\.
- **Rate Limiting:** Protects the login and registration endpoints from brute-force attacks.

