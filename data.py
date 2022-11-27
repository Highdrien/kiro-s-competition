import json

size = 'tiny'
with open(f"./sujet/{size}.json", 'r') as file:
  DATA = json.loads(file.read())

UNIT_PENALTY = DATA['parameters']['costs']['unit_penalty']
TARDINESS = DATA['parameters']['costs']['tardiness']