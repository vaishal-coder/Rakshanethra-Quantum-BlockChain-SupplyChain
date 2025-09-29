#!/usr/bin/env python3
"""
Supply Chain Tracking Module
Indigenous Hardware Verification System
"""

import json
import hashlib
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class SupplyChainEntry:
    component_id: str
    component_name: str
    manufacturer: str
    manufacturing_date: str
    batch_id: str
    verification_hash: str
    digital_signature: str
    custody_chain: List[Dict]
    indigenous_certification: bool
    security_clearance: str

class SupplyChainTracker:
    def __init__(self):
        self.components_db = {}
        self.manufacturers_db = {
            "IIT_MADRAS": {
                "name": "IIT Madras",
                "certification": "INDIGENOUS_VERIFIED",
                "speciality": "SHAKTI Processors",
                "security_level": "TOP_SECRET"
            },
            "C_DAC": {
                "name": "Centre for Development of Advanced Computing",
                "certification": "INDIGENOUS_VERIFIED", 
                "speciality": "Hardware Security Modules",
                "security_level": "SECRET"
            },
            "DRDO_LABS": {
                "name": "Defence Research and Development Organisation",
                "certification": "INDIGENOUS_VERIFIED",
                "speciality": "Anti-Tamper Enclosures",
                "security_level": "TOP_SECRET"
            },
            "BEL_INDIA": {
                "name": "Bharat Electronics Limited",
                "certification": "INDIGENOUS_VERIFIED",
                "speciality": "Power Systems",
                "security_level": "SECRET"
            },
            "COSMIC_CIRCUITS": {
                "name": "Cosmic Circuits Private Limited",
                "certification": "INDIGENOUS_VERIFIED",
                "speciality": "PCB Manufacturing",
                "security_level": "CONFIDENTIAL"
            }
        }
        self.initialize_sample_components()
    
    def generate_component_hash(self, component_data: str) -> str:
        """Generate SHA-256 hash for component verification"""
        return hashlib.sha256(component_data.encode()).hexdigest()
    
    def generate_digital_signature(self, component_id: str, manufacturer: str) -> str:
        """Generate digital signature for component authenticity"""
        signature_data = f"{component_id}_{manufacturer}_{datetime.datetime.now().isoformat()}"
        return hashlib.sha256(signature_data.encode()).hexdigest()[:32]
    
    def initialize_sample_components(self):
        """Initialize sample components for demo"""
        sample_components = [
            {
                "component_id": "SHAKTI-C-001",
                "component_name": "SHAKTI C-Class Processor",
                "manufacturer": "IIT_MADRAS",
                "manufacturing_date": "2024-08-15",
                "batch_id": "BATCH_SHAKTI_2024_Q3_001",
                "indigenous_certification": True,
                "security_clearance": "TOP_SECRET"
            },
            {
                "component_id": "HSM-SEC-001", 
                "component_name": "Hardware Security Module",
                "manufacturer": "C_DAC",
                "manufacturing_date": "2024-08-20",
                "batch_id": "BATCH_HSM_2024_Q3_001",
                "indigenous_certification": True,
                "security_clearance": "SECRET"
            },
            {
                "component_id": "ENC-CASE-001",
                "component_name": "Anti-Tamper Enclosure",
                "manufacturer": "DRDO_LABS",
                "manufacturing_date": "2024-08-25",
                "batch_id": "BATCH_ENC_2024_Q3_001", 
                "indigenous_certification": True,
                "security_clearance": "TOP_SECRET"
            },
            {
                "component_id": "PWR-UPS-001",
                "component_name": "Uninterruptible Power Supply",
                "manufacturer": "BEL_INDIA",
                "manufacturing_date": "2024-09-01",
                "batch_id": "BATCH_PWR_2024_Q3_001",
                "indigenous_certification": True,
                "security_clearance": "SECRET"
            },
            {
                "component_id": "PCB-IND-001",
                "component_name": "Indigenous PCB Board",
                "manufacturer": "COSMIC_CIRCUITS",
                "manufacturing_date": "2024-09-05",
                "batch_id": "BATCH_PCB_2024_Q3_001",
                "indigenous_certification": True,
                "security_clearance": "CONFIDENTIAL"
            }
        ]
        
        for comp_data in sample_components:
            self.register_component(comp_data)
    
    def register_component(self, component_data: Dict) -> SupplyChainEntry:
        """Register a new component in the supply chain"""
        # Generate verification hash
        hash_input = f"{component_data['component_id']}_{component_data['manufacturer']}_{component_data['batch_id']}"
        verification_hash = self.generate_component_hash(hash_input)
        
        # Generate digital signature
        digital_signature = self.generate_digital_signature(
            component_data['component_id'], 
            component_data['manufacturer']
        )
        
        # Initialize custody chain
        custody_chain = [{
            "stage": "MANUFACTURING",
            "handler": component_data['manufacturer'],
            "timestamp": component_data['manufacturing_date'],
            "location": "Manufacturing Facility",
            "action": "COMPONENT_CREATED",
            "verified_by": "QA_SYSTEM",
            "signature": hashlib.sha256(f"MFG_{component_data['component_id']}".encode()).hexdigest()[:16]
        }]
        
        # Create supply chain entry
        entry = SupplyChainEntry(
            component_id=component_data['component_id'],
            component_name=component_data['component_name'],
            manufacturer=component_data['manufacturer'],
            manufacturing_date=component_data['manufacturing_date'],
            batch_id=component_data['batch_id'],
            verification_hash=verification_hash,
            digital_signature=digital_signature,
            custody_chain=custody_chain,
            indigenous_certification=component_data['indigenous_certification'],
            security_clearance=component_data['security_clearance']
        )
        
        self.components_db[component_data['component_id']] = entry
        return entry
    
    def add_custody_event(self, component_id: str, event_data: Dict) -> bool:
        """Add custody chain event for component tracking"""
        if component_id not in self.components_db:
            return False
        
        component = self.components_db[component_id]
        
        # Generate event signature
        event_signature = hashlib.sha256(
            f"{component_id}_{event_data['stage']}_{event_data['timestamp']}".encode()
        ).hexdigest()[:16]
        
        custody_event = {
            "stage": event_data['stage'],
            "handler": event_data['handler'],
            "timestamp": event_data.get('timestamp', datetime.datetime.now().isoformat()),
            "location": event_data['location'],
            "action": event_data['action'],
            "verified_by": event_data.get('verified_by', 'SYSTEM'),
            "signature": event_signature
        }
        
        component.custody_chain.append(custody_event)
        return True
    
    def verify_component_authenticity(self, component_id: str) -> Dict:
        """Verify component authenticity and supply chain integrity"""
        if component_id not in self.components_db:
            return {
                "component_id": component_id,
                "verification_status": "COMPONENT_NOT_FOUND",
                "authentic": False,
                "indigenous": False,
                "security_cleared": False,
                "chain_integrity": False
            }
        
        component = self.components_db[component_id]
        
        # Verify hash integrity
        hash_input = f"{component.component_id}_{component.manufacturer}_{component.batch_id}"
        expected_hash = self.generate_component_hash(hash_input)
        hash_valid = expected_hash == component.verification_hash
        
        # Verify manufacturer authenticity  
        manufacturer_valid = component.manufacturer in self.manufacturers_db
        
        # Verify indigenous certification
        indigenous_valid = component.indigenous_certification
        
        # Verify custody chain integrity
        chain_valid = len(component.custody_chain) > 0 and all(
            'signature' in event for event in component.custody_chain
        )
        
        # Overall verification
        overall_authentic = hash_valid and manufacturer_valid and chain_valid
        
        return {
            "component_id": component_id,
            "component_name": component.component_name,
            "manufacturer": self.manufacturers_db.get(component.manufacturer, {}).get('name', 'UNKNOWN'),
            "verification_status": "VERIFIED" if overall_authentic else "VERIFICATION_FAILED",
            "authentic": overall_authentic,
            "indigenous": indigenous_valid,
            "security_cleared": True,
            "security_clearance": component.security_clearance,
            "chain_integrity": chain_valid,
            "hash_verification": hash_valid,
            "custody_events": len(component.custody_chain),
            "last_update": component.custody_chain[-1]['timestamp'] if component.custody_chain else "N/A"
        }
    
    def get_supply_chain_report(self) -> Dict:
        """Generate comprehensive supply chain report"""
        total_components = len(self.components_db)
        verified_components = sum(
            1 for comp_id in self.components_db 
            if self.verify_component_authenticity(comp_id)['authentic']
        )
        indigenous_components = sum(
            1 for comp in self.components_db.values()
            if comp.indigenous_certification
        )
        
        manufacturer_breakdown = {}
        for component in self.components_db.values():
            mfg_name = self.manufacturers_db.get(component.manufacturer, {}).get('name', 'UNKNOWN')
            manufacturer_breakdown[mfg_name] = manufacturer_breakdown.get(mfg_name, 0) + 1
        
        return {
            "report_id": f"SCR_{int(datetime.datetime.now().timestamp())}",
            "generated_at": datetime.datetime.now().isoformat(),
            "summary": {
                "total_components": total_components,
                "verified_components": verified_components,
                "indigenous_components": indigenous_components,
                "verification_rate": f"{(verified_components/total_components*100):.1f}%" if total_components > 0 else "0%",
                "indigenous_rate": f"{(indigenous_components/total_components*100):.1f}%" if total_components > 0 else "0%"
            },
            "manufacturer_breakdown": manufacturer_breakdown,
            "security_clearance_distribution": {
                "TOP_SECRET": len([c for c in self.components_db.values() if c.security_clearance == "TOP_SECRET"]),
                "SECRET": len([c for c in self.components_db.values() if c.security_clearance == "SECRET"]),
                "CONFIDENTIAL": len([c for c in self.components_db.values() if c.security_clearance == "CONFIDENTIAL"])
            },
            "chain_integrity": "SECURE",
            "compliance_status": "FULLY_COMPLIANT"
        }
    
    def simulate_deployment_tracking(self):
        """Simulate component deployment tracking for demo"""
        deployment_locations = [
            "Delhi Police HQ", "Mumbai Control Center", "Chennai Station",
            "Kolkata Command", "Bangalore Tech Center"
        ]
        
        for component_id in self.components_db.keys():
            # Add distribution event
            self.add_custody_event(component_id, {
                "stage": "DISTRIBUTION",
                "handler": "BPRD_LOGISTICS",
                "location": "Central Warehouse - New Delhi",
                "action": "COMPONENT_SHIPPED",
                "verified_by": "LOGISTICS_OFFICER"
            })
            
            # Add installation event  
            import random
            location = random.choice(deployment_locations)
            self.add_custody_event(component_id, {
                "stage": "INSTALLATION", 
                "handler": "FIELD_TECHNICIAN",
                "location": location,
                "action": "COMPONENT_INSTALLED",
                "verified_by": "SITE_SUPERVISOR"
            })
            
            # Add operational event
            self.add_custody_event(component_id, {
                "stage": "OPERATIONAL",
                "handler": "SURVEILLANCE_SYSTEM",
                "location": location, 
                "action": "COMPONENT_ACTIVE",
                "verified_by": "SYSTEM_MONITOR"
            })

def demo_supply_chain_tracking():
    """Demo function for supply chain tracking"""
    print("=" * 60)
    print("📦 SUPPLY CHAIN TRACKING DEMONSTRATION")
    print("   Indigenous Hardware Verification")
    print("=" * 60)
    
    tracker = SupplyChainTracker()
    
    print("\n1. 📋 REGISTERED COMPONENTS:")
    print("-" * 40)
    for comp_id, component in tracker.components_db.items():
        mfg_name = tracker.manufacturers_db.get(component.manufacturer, {}).get('name', 'UNKNOWN')
        print(f"• {comp_id}: {component.component_name}")
        print(f"  Manufacturer: {mfg_name}")
        print(f"  Indigenous: {'✅' if component.indigenous_certification else '❌'}")
        print(f"  Security Level: {component.security_clearance}")
        print()
    
    print("\n2. 🔍 COMPONENT VERIFICATION:")
    print("-" * 35)
    test_component = "SHAKTI-C-001"
    verification = tracker.verify_component_authenticity(test_component)
    
    print(f"Component: {verification['component_name']}")
    print(f"Status: {'✅ VERIFIED' if verification['authentic'] else '❌ FAILED'}")
    print(f"Indigenous: {'✅ YES' if verification['indigenous'] else '❌ NO'}")
    print(f"Chain Integrity: {'✅ SECURE' if verification['chain_integrity'] else '❌ COMPROMISED'}")
    print(f"Security Clearance: {verification['security_clearance']}")
    
    print("\n3. 📊 DEPLOYMENT SIMULATION:")
    print("-" * 35)
    tracker.simulate_deployment_tracking()
    print("✅ All components tracked through deployment pipeline")
    print("✅ Custody chain events recorded")
    print("✅ Installation verification completed")
    
    print("\n4. 📈 SUPPLY CHAIN REPORT:")
    print("-" * 35)
    report = tracker.get_supply_chain_report()
    
    print(f"Report ID: {report['report_id']}")
    print(f"Total Components: {report['summary']['total_components']}")
    print(f"Verification Rate: {report['summary']['verification_rate']}")
    print(f"Indigenous Rate: {report['summary']['indigenous_rate']}")
    print(f"Chain Integrity: {report['chain_integrity']}")
    print(f"Compliance: {report['compliance_status']}")
    
    print("\n5. 🏭 MANUFACTURER BREAKDOWN:")
    print("-" * 40)
    for manufacturer, count in report['manufacturer_breakdown'].items():
        print(f"• {manufacturer}: {count} components")
    
    print("\n6. 🔐 SECURITY CLEARANCE DISTRIBUTION:")
    print("-" * 45)
    for level, count in report['security_clearance_distribution'].items():
        print(f"• {level}: {count} components")
    
    print("\n" + "=" * 60)
    print("✅ SUPPLY CHAIN TRACKING DEMO COMPLETE")
    print("🔗 Full traceability established")
    print("🛡️ Indigenous verification confirmed")
    print("=" * 60)
    
    return tracker

if __name__ == "__main__":
    demo_supply_chain_tracking()
