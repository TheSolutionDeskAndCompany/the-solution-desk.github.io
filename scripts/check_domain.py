#!/usr/bin/env python3
"""
Domain configuration checker for The Solution Desk.

This script verifies that the domain configuration is correct for production.
"""
import os
import sys
import socket
import ssl
import dns.resolver
import requests
from urllib.parse import urlparse
from datetime import datetime, timezone

# Domain to check
DOMAIN = "thesolutiondesk.ca"
WWW_DOMAIN = f"www.{DOMAIN}"
RENDER_DOMAIN = "thesolutiondesk.onrender.com"

def check_dns(domain):
    """Check DNS records for the domain."""
    print(f"\n🔍 Checking DNS for {domain}...")
    try:
        # Check A records
        a_records = dns.resolver.resolve(domain, 'A')
        print(f"✅ A records: {', '.join([str(r) for r in a_records])}")
        
        # Check CNAME records
        try:
            cname_records = dns.resolver.resolve(domain, 'CNAME')
            print(f"✅ CNAME records: {', '.join([str(r.target) for r in cname_records])}")
        except dns.resolver.NoAnswer:
            print("ℹ️  No CNAME records found")
            
        # Check MX records
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            print(f"✅ MX records: {', '.join([str(r.exchange) for r in mx_records])}")
        except dns.resolver.NoAnswer:
            print("ℹ️  No MX records found (this is fine if you're not handling email)")
            
        # Check TXT records (for verification, SPF, etc.)
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            print("✅ TXT records:")
            for r in txt_records:
                print(f"   - {r}")
        except dns.resolver.NoAnswer:
            print("ℹ️  No TXT records found")
            
    except Exception as e:
        print(f"❌ DNS check failed: {e}")
        return False
    return True

def check_ssl(domain):
    """Check SSL certificate for the domain."""
    print(f"\n🔐 Checking SSL for {domain}...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Check expiration
                expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expire_date - datetime.now(timezone.utc)).days
                expiry_status = "✅" if days_until_expiry > 30 else "⚠️ "
                print(f"{expiry_status} SSL certificate expires on {expire_date.strftime('%Y-%m-%d')} "
                      f"({days_until_expiry} days remaining)")
                
                # Check issuer
                issuer = dict(x[0] for x in cert['issuer'])
                print(f"✅ Issuer: {issuer.get('organizationName', 'Unknown')}")
                
                # Check subject alternative names
                san = ""
                for ext in cert.get('subjectAltName', []):
                    if ext[0].lower() == 'dns':
                        san += f"{ext[1]} "
                if san:
                    print(f"✅ Subject Alternative Names: {san.strip()}")
                
                # Check protocol version
                print(f"✅ Protocol: {ssock.version()}")
                
    except Exception as e:
        print(f"❌ SSL check failed: {e}")
        return False
    return True

def check_http_redirects():
    """Check HTTP to HTTPS redirects and www redirects."""
    print("\n🔄 Checking HTTP redirects...")
    
    # Check HTTP -> HTTPS redirect
    try:
        r = requests.get(f"http://{DOMAIN}", allow_redirects=False, timeout=10)
        if r.status_code == 301 and r.headers.get('Location', '').startswith('https://'):
            print(f"✅ HTTP -> HTTPS redirect works")
        else:
            print(f"❌ HTTP -> HTTPS redirect failed (status: {r.status_code}, location: {r.headers.get('Location')})")
    except Exception as e:
        print(f"❌ HTTP check failed: {e}")
    
    # Check www -> non-www redirect (or vice versa, depending on your preference)
    try:
        r = requests.get(f"https://{WWW_DOMAIN}", allow_redirects=False, timeout=10)
        if r.status_code == 301 and r.headers.get('Location', '').startswith(f'https://{DOMAIN}'):
            print(f"✅ {WWW_DOMAIN} -> {DOMAIN} redirect works")
        else:
            print(f"⚠️  {WWW_DOMAIN} does not redirect to {DOMAIN} (status: {r.status_code}, location: {r.headers.get('Location')})")
    except Exception as e:
        print(f"❌ {WWW_DOMAIN} check failed: {e}")

def check_render_config():
    """Check if Render service is properly configured for the custom domain."""
    print("\n⚙️  Checking Render configuration...")
    
    # This is a placeholder for actual Render API checks
    # In a real implementation, you would use the Render API to verify:
    # 1. Custom domain is properly configured in Render
    # 2. SSL certificate is provisioned for the custom domain
    # 3. DNS records point to the correct Render service
    
    print("ℹ️  Note: Run this on Render's infrastructure or with RENDER_API_KEY "
          "to verify Render-specific settings")

def main():
    print(f"🌐 Domain Configuration Check for {DOMAIN}")
    print("=" * 50)
    
    # Check DNS records
    dns_ok = check_dns(DOMAIN)
    
    # Check www subdomain DNS
    www_dns_ok = check_dns(WWW_DOMAIN)
    
    # Check SSL certificates
    ssl_ok = check_ssl(DOMAIN)
    
    # Check redirects
    check_http_redirects()
    
    # Check Render configuration
    check_render_config()
    
    print("\n" + "=" * 50)
    print("✅ Domain check completed!")
    
    if not all([dns_ok, www_dns_ok, ssl_ok]):
        print("\n⚠️  Some checks failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
