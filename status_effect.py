class StatusEffect:
    def __init__(self, name, duration, description):
        self.name = name
        self.duration = duration
        self.description = description
        self.effects = {
            "strength": 0,
            "percent_strength": 0,
            "defense": 0,
            "percent_defense": 0,
            "resistance": 0,
            "percent_resistance": 0,
            "dexterity": 0,
            "percent_dexterity": 0,
            "speed": 0,
            "percent_speed": 0,
            "luck": 0,
            "percent_luck": 0
        }

    def __str__(self):
        return f"{self.name}: {self.description} ({self.duration} Turn/s)\n" + self.read_effects()

    def __repr__(self):
        return f"StatusEffect(name={self.name}, duration={self.duration}, description={self.description}, effects={self.effects})"

    def read_effects(self):
        effects = ""
        for key in self.effects:
            if self.effects[key] != 0:
                if self.effects[key] > 0:
                    effects += f"{key.capitalize()}: +{self.effects[key]}"
                elif self.effects[key] < 0:
                    effects += f"{key.capitalize()}: {self.effects[key]}"
                if "percent" in key:
                    effects += "%"
                effects += "\n"
        return effects

    def apply_effect(self, stat, value):
        if stat in self.effects:
            self.effects[stat] = value
        else:
            print("Invalid stat!")

testingStatusEffect = StatusEffect("Testing", 3, "Testing Effects")
testingStatusEffect.apply_effect("strength", 10)

testingStatusEffect2 = StatusEffect("More Testing", 1, "Bees")
testingStatusEffect2.apply_effect("percent_strength", -10)

hardenEffect = StatusEffect("Harden", 3, "Minor defense increase")
hardenEffect.apply_effect("defense", 10)

resistEffect = StatusEffect("Resist", 3, "Minor resistance increase")
resistEffect.apply_effect("resistance", 10)

accuracyEffect = StatusEffect("Accuracy", 3, "Minor dexterity increase")
accuracyEffect.apply_effect("dexterity", 20)

speedEffect = StatusEffect("Speed", 3, "Minor speed increase")
speedEffect.apply_effect("speed", 10)

luckyEffect = StatusEffect("Lucky", 3, "Minor luck increase")
luckyEffect.apply_effect("luck", 70)