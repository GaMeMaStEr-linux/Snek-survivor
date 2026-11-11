import pygame

class Wavemanager :
    def __init__(self):
        self.current_wave = 1
        self.state = "DODGE"
        self.dodge_duration = 10.0
        self.rest_duration = 5.0
        self.time_remaining = self.dodge_duration
    def update(self, dt):
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.advance_state()

    def advance_state(self):
        if self.state == "DODGE":
            self.state = "REST"
            self.time_remaining = self.rest_duration
        elif self.state == "REST":
            self.complete_rest()

    def complete_rest(self):
        if self.state == "REST":
            self.current_wave += 1
            self.dodge_duration += 1.0
            self.rest_duration -= 0.5
            self.state = "DODGE"
            self.time_remaining = self.dodge_duration
