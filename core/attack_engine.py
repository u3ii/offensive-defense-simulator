import json
import time
import random
from datetime import datetime

class AttackEngine:
    def __init__(self, scenario_file):
        with open(scenario_file, 'r', encoding='utf-8') as f:
            self.scenario = json.load(f)
        
        self.results = {
            'scenario_name': self.scenario.get('scenario_name', 'Unknown'),
            'difficulty': self.scenario.get('difficulty', 'Unknown'),
            'time': str(datetime.now()),
            'phases': [],
            'ai_decisions': [],
            'vulnerabilities_found': [],
            'recommendations': []
        }
        
        self.use_ai = True

    def run(self):
        if 'targets' in self.scenario:
            for target in self.scenario['targets']:
                for service in target.get('services', []):
                    if service.get('risk') in ['high', 'critical']:
                        self.results['vulnerabilities_found'].append(service)
        else:
            for service in self.scenario.get('target', {}).get('services', []):
                if service.get('risk') in ['high', 'critical']:
                    self.results['vulnerabilities_found'].append(service)
        
        return self.results