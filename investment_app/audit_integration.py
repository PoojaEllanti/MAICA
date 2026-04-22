import sys
import os
import json

# allow access to parent folder (MAICA80)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.coordinator_agent import generate_final_report

def run_maica_audit(portfolio):

    # call MAICA coordinator
    report = generate_final_report("finance")

    return report