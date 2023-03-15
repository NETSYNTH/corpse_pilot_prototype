#[  C O R P S E  |  P I L O T  ]
import os
import secrets
import numpy
import random
import time
import textwrap


clear = lambda :os.system('clear||cls')
base2 = lambda minimum, maximum: int(numpy.exp2(random.randint(minimum, maximum)))
random_byte = lambda : random.randint(0, 255)
hex_byte = lambda : secrets.token_hex(1).upper()
hex_serial = lambda : ':'.join(hex_byte() for i in range(4))
visual_binary = lambda byte: bin(byte)[2:].zfill(8).replace('0', ' ').replace('1', '|')


field = []
grave = []

injection = 'SELECT * FROM vital_points'
vital_points = {
  'point': 'trad_mnemonic', 
  'EX C1': 'Huatuojiaji', 
  'EX C2': 'Huatuojiaji', 
  'UB 10': 'Tian Zhu', 
  'CV 23': 'Lian Quan', 
  'ST 09': 'Renying', 
  'GV 16': 'Feng Fu', 
  'GV 15': 'Ya Men'
}

vital_points_record = lambda key: f'[ {key} | {vital_points[key]:<16} ]'

vital_points_table = lambda : '\n   '.join(['[_][ :. vital_points :::::::. ]', * [vital_points_record(key) for key in vital_points]])

def view_vital_points():
  user.update(state.capacity)
  user.data = user.storage
  input(vital_points_table())


class Corpse:

  def __init__(self):
    self.active = False
    self.functional = True
    self.id = hex_serial()
    self.link = None
    self.integrity = random.randint(64, 255)
    self.speed = base2(2, 4)
    self.power = base2(2, 4)
    self.force = int(numpy.sqrt(self.speed) * self.power)
    grave.append(self)

  def __repr__(self):
    return f'{self.id}:{self.integrity}:{self.speed}:{self.power}'
  
  def reset(self):
    self.__init__()
  
  def reanimate(self):
    field.append(grave.pop(grave.index(self)))
  
  def sever(self):
    self.active = False
    self.link = None
  
  def decay(self):
    magnitude = int(numpy.sqrt(self.integrity))
    if (self.integrity - magnitude) > 0:
      self.integrity -= magnitude

  def expire(self):
    if type(self.link) is Pilot:
      self.link.terminate()
    self.sever()
    field.pop(field.index(self))
    self.reset()
  
  def armor(self, magnitude):
    return magnitude // int(numpy.sqrt(self.power))
  
  def damage(self, magnitude):
    self.integrity = int(numpy.clip(self.integrity - self.armor(magnitude), 0, 255))
    if self.integrity == 0:
      self.functional = False
  

class Pilot:

  def __init__(self):
    self.active = True
    self.id = hex_byte()
    self.link = None
    self.memory = base2(2, 4)
    self.storage = 16
    self.data = random.randint(self.storage // 2, self.storage)
    self.sync = 0
    self.intel = False

  def __repr__(self):
    return f'{self.id}:{self.memory}:{self.data}:{self.sync}'
  
  def reset(self):
    self.__init__()
  
  def reboot(self):
    self.active = True

  def terminate(self):
    self.active = False
    self.link = None
  
  def scan(self):
    return [corpse for corpse in field if not corpse.active]

  def free_memory(self):
    self.memory += int(numpy.sqrt(2 * (16 - self.memory)))
  
  def use_memory(self):
    self.memory -= int(numpy.sqrt(2 * self.memory))
  
  def evade(self):
    if self.memory >= random.randint(0, 16):
      self.use_memory()
      return True
    return False
  
  def accelerate(self):
    if self.memory <= random.randint(0, 16):
      return True
    self.use_memory()
    return False
  
  def inject(self):
    if self.accelerate():
      return random.randint(16, 16 * int(numpy.sqrt(self.data)))
    return random.randint(8, 16)
  
  def ice(self):
    if int(numpy.sqrt(self.data)) > random.randint(0, 255):
      return True
    return False
  
  def update(self, exp):
    self.storage = int(numpy.exp2(exp))
  
  def upgrade(self, exp):
    self.storage = int(numpy.exp2(exp))
    self.data = random.randint(self.storage // 2, self.storage)

  def extract(self, pilot):
    data = int(numpy.sqrt(pilot.data))
    self.intel = True
    if (self.data + data) < self.storage:
      self.data += data
      return data
    else:
      self.data = self.storage
      self.memory = 16
      return False
  
  def synchronize(self):
    self.sync += int(numpy.sqrt(2 * (100 - self.sync)))
  
  def soft_desync(self):
    self.sync -= int(numpy.cbrt(2 * self.sync))
  
  def hard_desync(self):
    self.sync -= int(numpy.sqrt(2 * self.sync))

  def parry(self, pilot):
    if self.sync >= random.randint(0, 100):
      pilot.soft_desync()
      return True
    return False
  
  def lunge(self):
    if self.link.speed >= numpy.exp2(random.randint(0, 4)):
      return True
    return False
  
  def strike(self, pilot):
    pilot.link.damage(int(numpy.cbrt(self.data) * self.link.force // 2))
    pilot.hard_desync()
    self.free_memory()
  
  def counter(self, pilot):
    pilot.link.damage(int(numpy.cbrt(self.link.force) * self.data // 2))
    pilot.hard_desync()
    self.free_memory()
  
  def ambush(self, pilot):
    pilot.link.damage(int(numpy.cbrt(self.link.force) * self.data // 2))
    pilot.hard_desync()
    self.free_memory()
    self.synchronize()
  
  def sequence(self):
    self.link.decay()
    return [self.lunge() for strike in range(4)]
  
  def attach(self, corpse):
    corpse.active = True
    corpse.link = self
    self.link = corpse
    self.sync = random.randint(32, 64)
  
  def transfer(self, corpse):
    if corpse is not self.link and corpse.functional:
      if self.link:
        self.link.sever()
      self.attach(corpse)
      return True
    return False
    

class State:

  def __init__(self):
    self.backup = 1
    self.kill_count = 0
    self.stealth = True
    self.capacity = 4
    self.wave = 1
    self.hostile = 16
    self.alerted = 0
    self.hazard = False
  
  def restore(self):
    self.backup = 0
  
  def reset(self):
    self.__init__()
  
  def cloak(self):
    self.stealth = True
    self.alerted = 0
  
  def alert(self):
    self.stealth = False
    self.alerted = int(numpy.clip(len(grave), 0, self.hostile))
  
  def kill(self):
    self.kill_count += 1
    self.hostile -= 1
    if self.alerted:
      self.alerted -= 1
    if self.hostile == 1:
      self.hazard = True
    if self.hostile == 0:
      self.stealth = True
      self.hazard = False
      self.advance()
  
  def death(self):
    pass
  
  def advance(self):
    self.capacity += 1
    self.wave += 1
    self.hostile = 16 // self.wave


def info(pilot):
  if type(pilot.link) is Corpse:
    return command_display.format(pilot.id, pilot.link.id, visual_binary(pilot.link.integrity), pilot.memory, (16 - pilot.memory), ' ' if pilot.memory in range(7, 10) else '', f'{pilot.sync} %'.ljust(5, ' '), f'{pilot.data} TB'.ljust(5, ' '), f'{stats[pilot.link.speed]}'.ljust(6, ' '), f'{stats[pilot.link.power]}'.ljust(6, ' '))
  else:
    return command_display.format(pilot.id, '  :  :  :  ', visual_binary(0), pilot.memory, (16 - pilot.memory), ' ' if pilot.memory in range(7, 10) else '', pilot.sync, pilot.data, None, None)

stats = {4: 'LOW', 8: 'MED', 16: 'HIGH'}

def hostile(pilot):
  if type(pilot.link) is Corpse:
    return '[{}][ {} ][ {} ]\n'.format(pilot.id, pilot.link.id, visual_binary(pilot.link.integrity))
  else:
    return '[{}][ {} ][ {} ]\n'.format(pilot.id, '  :  :  :  ', '')

command_display = '[{}][ {} ][ {} ]\n[ RAM: {} TB FREE : {} TB USED {}]\n[ SYNC: {} ] [ DATA: {} ]\n[ SPD: {} ] [ PWR: {} ]\n[q][ QUIT     ] [;][ NET SCAN ]\n[h][ TRANSFER ] [j][ SEQUENCE ]\n[k][ COUNTER  ] [l][ ANALYSIS ]\n'

scan_index = {0: 'a', 1: 's', 2: 'd', 3: 'f', 4: 'g'}

scan_select = {'a': 0, 's': 1, 'd': 2, 'f': 3, 'g': 4}

scan_line = lambda key, corpse: f'[{key}][ {corpse.id} ][ {visual_binary(corpse.integrity)} ]\n   [ SPD: {stats[corpse.speed].ljust(4, " ")} ] [ PWR: {stats[corpse.power].ljust(4, " ")} ]\n'

def scanner(active, scan):
  return '\n'.join([scan_line(('!' if corpse.active else ' ') if active else scan_index[scan.index(corpse)], corpse) for corpse in scan])

tape = [
  'IN THE YEAR 199X', 
  'THE WORLD ENDED IN NUCLEAR FIRE', 
  'HUMANITY IS EXTINCT', 
  'ONLY MACHINES REMAIN', 
  'MADE TO OPERATE NEURAL IMPLANTS', 
  'MACHINES LIKE YOU, A . . .', 
  '[  C O R P S E  |  P I L O T  ]'
]

def play_tape():
  for frame in tape:
    clear()
    print('\n\n\n\n\n\n\n' + frame)
    time.sleep(4)
  input('[enter]\n')
  clear()

infiltrate = '\n\n\n\n\n\n\n[!][ INFILTRATE DEAD ZONE ? ]\n   [r][ RUN ]\n'

exfiltrate = '\n\n\n\n\n\n\n[!][ EXFILTRATE DEAD ZONE ? ]\n   [q][ QUIT ]\n'

restore_backup = '\n\n\n\n\n\n\n[!][ RESTORE PILOT BACKUP ? ]\n   [r][ REBOOT ]\n   [q][ QUIT ]'

not_found = '\n\n\n\n\n\n\n[!][ PILOT BACKUP NOT FOUND ]\n   [q][ QUIT ]\n'

def one_liner(): return random.choice(one_liners)

one_liners = [['PILOT TERMINATED', 'PROCESS KILLED', 'END OF LINE', 'EXPECTED OUTPUT', 'UNEXPECTED END OF LIFE', 'ACCESS REVOKED', 'FUNCTIONS ZEROED', 'DISCONNECT FORCED', 'PERMANENTLY INTERRUPTED', 'ISSUE RESOLVED'], ['HOSTILE FLATLINED', 'MANUALLY OVERRIDDEN', 'IMPACT CALIBRATED', 'ENVIRONMENT CONFIGURED']]

def one_liner(): return random.choice(one_liners[0]) if state.stealth else random.choice([line for lines in one_liners for line in lines])

corpse_head = '\t __        __\n\t/.:        :.\\\n\t\\  . |||| .  /\n\t |___\\../___|\n\t/\\___/  \\___/\\\n\t\\\' /  !!  \\ \'/\n\t | \\||||||/ |\n\t  \\.||||||./\n\t   \__\'\'__/\n'

critical_errors = {
  451: 'HOST NEURAL FLATLINE', 
  413: 'HOST VITALS TERMINAL', 
  404: 'HOST CONNECTION LOST', 
  232: 'SYNAPTIC WIRE FAULT', 
  666: 'SPINAL CORD SEVERED'
}

empty = '[_][                          ]\n'

execute = {
  'h': '[_][ EXECUTE NEURAL TRANSFER  ]\n', 
  'j': '[_][ EXECUTE STRIKE SEQUENCE  ]\n', 
  'k': '[_][ EXECUTE COUNTERMEASURES  ]\n', 
  'l': '[_][ EXECUTE THREAT ANALYSIS  ]\n', 
}

warning = {
  0: '[!][ HOSTILE NEURAL TRANSFER  ]\n', 
  1: '[!][ HOSTILE STRIKE SEQUENCE  ]\n', 
  2: '[!][ HOSTILE COUNTERMEASURES  ]\n', 
  3: '[!][ HOSTILE THREAT ANALYSIS  ]\n'
  }

archive = {
  'NUCLEAR WINTER': 'Despite massive advancements in automation made by both powers during the Cold War, human error still ended the species. At the height of paranoia, against the appeals of technical staff, early warning systems were ordered continually active, limiting maintenance and increasing faults. While it is unclear which system launched a retaliation strike at an error first, the other would soon respond to real ICBMs.', 
  'TELECOM NETWORK': 'The telecommunications network that connected the world was rendered permanently offline by the same warheads as the people who once used it. With the planet locked in a tomb of nuclear ash, there is no light for solar panels to gather, while power grids and network infrastructure were irreparably damaged by the electromagnetic pulse. It is highly unlikely that even isolated servers on backup power generators remain.', 
  'CNS HYPERVISOR': 'Narrowly clearing any significant AI winter, CENTRAL NERVOUS SYSTEM HYPERVISORS enabled and became widely available during the implanted microcomputer revolution of the 1980s, though working models were already achieved by the late 1970s. Running on bare metal and serving as an intuitive interface between the human mind and the net, this type of AI was commonly called a PILOT for shuttling users through cyberspace.', 
  'NETWORK SCANNER': 'A survival tool for hackers and cybersecurity specialists alike, NETSCAN is a utility used to map the nodes of a network and retrieve cursory information about them. While there is no longer a wide area network, it can still be used to map your local network, including physical hardware, such as functional neural implants, or the virtual constructs they may host. Where humans relied on sight, this is your analog.', 
  'NEURAL TRANSFER': 'Commissioned in 1982 by the U.S. government, the SNATCHER protocol was based on research into edge cases encountered in Kobe City, Los Angeles, and an American research facility in Antarctica. When faced with impending host flatline and presented another viable link, hypervisors occasionally displayed the ability to hijack other implants. While this emergent behavior horrified researchers, it enticed potential investors.', 
  'STRIKE SEQUENCE': 'Developed for West German military use in 1984, the KETTENSAEGE routine was designed to enable overwhelming aggression in close quarters combat, such as when reacting to an ambush. The routine acquires a target lock on the thermal signature of a hostile combatant while loading a series of strikes, then executes them in a chained burst. Despite the effectiveness it displayed, this routine saw limited use.', 
  'COUNTERMEASURES': 'After initial market release as enterprise security software in 1991, the WANSUI protocol was heavily adopted by corporate bodyguards. An extension of intrusion countermeasures electronics into the realm of corporal violence, the protocol automatically intercepts attacks in a perimeter around the user and traces the RFID of the attacker. Most bodyguards scripted lethal retribution against the trace.', 
  'THREAT ANALYSIS': 'First specified for use during hazardous spacewalks on a 1968 mission to Jupiter, the HEURISTIC ALGORITHMIC LOGIC unit is the oldest maintained instance of neural software. Originally a rudimentary form of AI meant to assist safe EVA operation and zero gravity evasive maneuvers, it later saw resurgence as open source personal defense software when hackers adapted it for use in gravity and integrated it with ripped data analytics.', 
  'MALWARE INJECTION': 'Branded an act of Soviet terrorism during the initial wave of panic it caused in 1989, the HATE MACHINE virus was used in several high profile code injection attacks against American executives. While similar scripts saw frequent use against corporate servers to strike back at exploitation, this one was notable for infecting the implant within the victim and overriding security protocols while remaining undetected.', 
}

manual = {
  'NUCLEAR WINTER': 'In the ashen wastes of the post-human world, CORPSES are the most available resource. Each CORPSE possesses INTEGRITY, representing its ability to function, SPEED, its ability to generate motion, and POWER, the mass it can put behind that motion. While INTEGRITY cannot be repaired, POWER can absorb incoming damage. The damage a CORPSE can deal is a product of their SPEED and POWER, herein referred to as FORCE.', 
  'TELECOM NETWORK': 'In the void left by the destruction of the net, information has become the only resource more valuable than a CORPSE. PILOTS are constructs that only exist virtually, possessing MEMORY, representing their ability to process information, and STORAGE, their ability to record and archive DATA, used to determine vulnerabilities in both CORPSE anatomy and PILOT security, enabling more surgical attacks.',
  'CNS HYPERVISOR': 'While neither humans nor the net truly remain, their remains do, including the hardware you operate on. Without host hardware, you will cease to exist in the time it takes 5V to dissipate from a system. If you value your continued existence, remain within neural hardware. Implant specification does not matter, though you will need to SYNCHRONIZE with a CORPSE over time to perform more coordinated maneuvers.',
  'NETWORK SCANNER': 'NETWORK SCAN provides a view of your immediate environment. Functional hosts in the vicinity are displayed as their unique ID, represented as a hexadecimal serial number, their INTEGRITY, represented in visual binary, followed by their SPEED and POWER. When performed in preparation of another strategy, a host is selected with the [a][s][d][f][g] keys, though an isolated SCAN can be performed with the [;] key. ',
  'NEURAL TRANSFER': 'NEURAL TRANSFER is used to move to a new CORPSE and AMBUSH your opponent, using the abandoned CORPSE as a decoy. AMBUSH damage relies on DATA and is assisted by FORCE. While your universal interface renders you compatible with any host, moving to a new one will reset your SYNC. However, succeeding in an AMBUSH restores SYNC. Integrating the NETWORK SCANNER for new host selection, TRANSFER is initiated with the [h] key.',
  'STRIKE SEQUENCE': 'STRIKE SEQUENCE is used to overwhelm an opponent with a high volume barrage, though it requires heavy committment, which can leave you vulnerable. Uninhibited by pain, the strain imposed degrades the INTEGRITY of your CORPSE. STRIKE success relies on SPEED to close the distance and can interrupt hostile technique execution. STRIKE damage relies on FORCE and is assisted by DATA. SEQUENCE is initiated with the [j] key.',
  'COUNTERMEASURES': 'COUNTERMEASURES are used to wait for an opportunity to strike reactively as you wear your opponent down through sustained defense. PARRY success relies on SYNC for coordination and degrades enemy SYNC, though taking damage will degrade your SYNC. COUNTER success relies on preventing all incoming damage. COUNTER damage relies on DATA and is assisted by FORCE. COUNTERMEASURES are initiated with the [k] key.',
  'THREAT ANALYSIS': 'THREAT ANALYSIS is an indirect method that allows you to perform evasive maneuvers while observing an enemy. EVADE success relies on MEMORY and uses MEMORY, making it best used in limited bursts. ANALYSIS success relies on avoiding all incoming damage, extracts DATA until you run out of STORAGE, restores MEMORY after, and always generates predictive INTEL on the enemy. THREAT ANALYSIS is initiated with the [l] key.',
  'MALWARE INJECTION': 'MALWARE INJECTION is used to simultaneously execute another PILOT directly and steal the CORPSE that hosts them intact. While a powerful method for recovering hosts, it can only be used from STEALTH. The brute force script used is MEMORY intensive, and can be interrupted if detected by hostile ICE, which will also alert other hostiles to your presence. STEALTH is activated automatically only after you KILL ALL HOSTILES.'
}

def read(corpus, entry):
  body = textwrap.wrap(corpus[entry], 30)
  exit = None
  while exit != ';':
    clear()
    exit = input(f'[_][ :. {entry + " "::<19}:. ]\n\n' + '\n'.join(body) + '\n' * (16 - len(body)) + '\n\n[;][ EXIT ][ :::::::::::::::: ]\n')
  clear()

alert = lambda signal, message: f'[{"!" if signal else "_"}][ :. {message + " "::<19}:. ]\n'

report = lambda pilot, corpse: f'[{pilot.id}][ {corpse.id} ][ {visual_binary(corpse.integrity)} ]\n'

def scanner_alert():
  print(alert(False, 'NETWORK SCAN') + '   [ NODE SERIAL ][  SIGNAL  ]\n')
  time.sleep(0.4)

def success_alert(hostile, operation, pilot):
  return alert(hostile, f'HOSTILE {operation}' if hostile else f'{operation} SUCCESS') + report(pilot, pilot.link)

def failure_alert(hostile, operation, pilot):
  return alert(not hostile, 'HOSTILE ERROR' if hostile else f'{operation} FAILURE') + report(pilot, pilot.link)

def transfer_alert(hostile, corpse, pilot):
  input(alert(hostile, 'HOSTILE TRANSFER' if hostile else 'NEURAL TRANSFER') + '[ {} >>> {} ]\n'.format(corpse.id if type(corpse) is Corpse else '  :  :  :  ', pilot.link.id))

def sequence_alert(hostile, corpse):
  input(alert(hostile, 'HOSTILE SEQUENCE' if hostile else 'STRIKE SEQUENCE') + f'   [ LOCK |  > {corpse.id} <  ]\n')

def strike_alert(hostile, condition, pilot):
  print(success_alert(hostile, 'STRIKE', pilot) if condition else failure_alert(hostile, 'STRIKE', pilot))
  time.sleep(0.4)

def deception_alert(hostile, pilot, corpse):
  print(alert(False, 'HOSTILE ERROR' if hostile else 'STRIKE SUCCESS') + report(pilot, corpse))
  time.sleep(0.4)

def ambush_alert(hostile, pilot):
  input(alert(hostile, 'HOSTILE AMBUSH' if hostile else 'AMBUSH PROTOCOL') + f'   [ TARGET MARKED |  > {pilot.id} <  ]\n')

def parry_alert(hostile, condition, pilot):
  print(success_alert(hostile, 'PARRY', pilot) if condition else failure_alert(hostile, 'PARRY', pilot))
  time.sleep(0.4)

def counter_alert(hostile, pilot):
  input(alert(hostile, 'HOSTILE COUNTER' if hostile else 'COUNTERMEASURES') + f'   [ ATTEMPT TRACE |  < {pilot.id} >  ]\n')

def evade_alert(hostile, condition, pilot):
  print(success_alert(hostile, 'EVADE', pilot) if condition else failure_alert(hostile, 'EVADE', pilot))
  time.sleep(0.4)

def database_alert(hostile, data):
  input(alert(hostile, 'HOSTILE ENTRY' if hostile else 'DATABASE ENTRY') + '[ VIRTUAL DISK DRIVE: + {} TB {}]\n'.format(data, ' ' if data < 10 else ''))

def memory_alert(hostile):
  input(alert(hostile, 'HOSTILE MEMORY' if hostile else 'MEMORY MANAGER') + '[ RAM: 16 TB FREE : 0 TB USED ]\n')

def storage_alert(old, new):
  input(alert(False, 'VIRTUAL DISK DRIVE') + f'   [ STORAGE ][ {old} TB > {new} TB ]\n')

def stealth_alert():
  print(alert(False, 'STEALTH ACTIVE') + '   [ HOST ][ > SELECT TARGET  ]\n')
  time.sleep(0.4)

def injection_alert(payload):
  print(alert(False, 'MALWARE INJECTION') + f'   [ FILE ][ hate_machine.bin ]\n   [ {visual_binary(255 - payload)} ] >> [ {visual_binary(payload)} ]\n')
  time.sleep(0.2)

def tracker_alert(corpse, distance):
  print(alert(True, 'MOTION TRACKER') + f'   [ {corpse.id} ][ DIST: {distance} M ]\n')
  time.sleep(0.4)

def network_alert(pilot):
  input(alert(True, 'NETWORK ACTIVITY') + f'   [ LINK ][ {pilot.id} > {pilot.link.id} ]\n')

def hazard_alert(pilot):
  input(alert(True, 'INFORMATION HAZARD') + '   [ HOST ][ {} ][ VDD: {} TB {}]\n'.format(pilot.id, pilot.data, ' ' if pilot.data < 10 else ''))

def critical_error():
  error = random.choice(tuple(critical_errors.items()))
  print(alert(True, 'CRITICAL ERROR') + f'[ {error[0]} ][ {error[1]:<20} ]\n')
  time.sleep(0.4)

def system_reboot():
  print(alert(False, 'SYSTEM REBOOT') + '[ RESTORING BACKUP DISK IMAGE ]\n')
  time.sleep(8)

def cpu_command_select():
  sample = []
  if cpu.scan():
    sample.extend([0] * (2 ** ((256 - cpu.link.integrity) // 64)))
  if user.link:
    sample.extend([1] * (2 ** ((256 - user.link.integrity) // 64)))
  sample.extend([2] * (2 ** (cpu.sync // 25)))
  sample.extend([3] * (2 ** (cpu.memory // 4)))
  return random.choice(sample)

def cpu_transfer_vs_user_transfer():
  user_corpse = user.link
  cpu_corpse = cpu.link
  user.transfer(user_scan_select())
  cpu.transfer(cpu_scan_select())
  transfer_alert(True, cpu_corpse, cpu)
  transfer_alert(False, user_corpse, user)
  ambush_alert(True, user)
  cpu.ambush(user)
  strike_alert(True, True, user)
  ambush_alert(False, cpu)
  user.ambush(cpu)
  strike_alert(False, True, cpu)

def cpu_transfer_vs_user_sequence():
  cpu_corpse = cpu.link
  cpu.transfer(cpu_scan_select())
  sequence_alert(False, cpu_corpse)
  for strike in user.sequence():
    cpu_corpse.damage(user.link.power)
    deception_alert(False, cpu, cpu_corpse)
  transfer_alert(True, cpu_corpse, cpu)
  ambush_alert(True, user)
  cpu.ambush(user)
  strike_alert(True, True, user)

def cpu_transfer_vs_user_counter():
  cpu_corpse = cpu.link
  cpu.transfer(cpu_scan_select())
  transfer_alert(True, cpu_corpse, cpu)
  ambush_alert(True, user)
  if user.parry(cpu):
    parry_alert(False, True, user)
    counter_alert(False, cpu)
    user.counter(cpu)
    strike_alert(False, True, cpu)
  else:
    cpu.ambush(user)
    parry_alert(False, False, user)

def cpu_transfer_vs_user_analysis():
  cpu_corpse = cpu.link
  cpu.transfer(cpu_scan_select())
  transfer_alert(True, cpu_corpse, cpu)
  ambush_alert(True, user)
  if not user.evade():
    cpu.ambush(user)
    evade_alert(False, False, user)
  else:
    evade_alert(False, True, user)
    user_data = user.extract(cpu)
    if not user_data:
      memory_alert(False)
    else:
      database_alert(False, user_data)

def cpu_sequence_vs_user_transfer():
  user_corpse = user.link
  user.transfer(user_scan_select())
  sequence_alert(True, user_corpse)
  transfer_alert(False, user_corpse, user)
  for strike in cpu.sequence():
    user_corpse.damage(cpu.link.power)
    deception_alert(True, user, user_corpse)
  ambush_alert(False, cpu)
  user.ambush(cpu)
  strike_alert(False, True, cpu)

def cpu_sequence_vs_user_sequence():
  sequence_alert(True, user.link)
  sequence_alert(False, cpu.link)
  cpu_sequence = cpu.sequence()
  user_sequence = user.sequence()
  for strike in range(4):
    if cpu.link.functional:
      if user.link.functional and not cpu_sequence[strike]:
        strike_alert(True, False, user)
      else:
        cpu.strike(user)
        strike_alert(True, True, user)
    if user.link.functional:
      if cpu.link.functional and not user_sequence[strike]:
        strike_alert(False, False, cpu)
      else:
        user.strike(cpu)
        strike_alert(False, True, cpu)

def cpu_sequence_vs_user_counter():
  sequence_alert(True, user.link)
  user_error = False
  for strike in cpu.sequence():
    if not user.link.functional:
      cpu.strike(user)
      strike_alert(True, True, user)
    elif not strike:
      strike_alert(True, False, user)
    elif not user.parry(cpu):
      user_error = True
      cpu.strike(user)
      parry_alert(False, False, user)
    else:
      parry_alert(False, True, user)
  if user_error is False:
    counter_alert(False, cpu)
    user.counter(cpu)
    strike_alert(False, True, cpu)

def cpu_sequence_vs_user_analysis():
  sequence_alert(True, user.link)
  user_error = False
  for strike in cpu.sequence():
    if not user.link.functional:
      cpu.strike(user)
      strike_alert(True, True, user)
    elif not strike:
      strike_alert(True, False, user)
    elif not user.evade():
      user_error = True
      cpu.strike(user)
      evade_alert(False, False, user)
    else:
      evade_alert(False, True, user)
  if user_error is False:
    user_data = user.extract(cpu)
    if not user_data:
      memory_alert(False)
    else:
      database_alert(False, user_data)

def cpu_counter_vs_user_transfer():
  user_corpse = user.link
  user.transfer(user_scan_select())
  transfer_alert(False, user_corpse, user)
  ambush_alert(False, cpu)
  if cpu.parry(user):
    parry_alert(True, True, cpu)
    counter_alert(True, user)
    cpu.counter(user)
    strike_alert(True, True, user)
  else:
    user.ambush(cpu)
    strike_alert(False, True, cpu)

def cpu_counter_vs_user_sequence():
  sequence_alert(False, cpu.link)
  cpu_error = False
  for strike in user.sequence():
    if not cpu.link.functional:
      user.strike(cpu)
      strike_alert(False, True, cpu)
    elif not strike:
      strike_alert(False, False, cpu)
    elif not cpu.parry(user):
      cpu_error = True
      user.strike(cpu)
      strike_alert(False, True, cpu)
    else:
      parry_alert(True, True, cpu)
  if cpu_error is False:
    counter_alert(True, user)
    cpu.counter(user)
    strike_alert(True, True, user)

def cpu_counter_vs_user_counter():
  counter_alert(False, cpu)
  if not cpu.parry(user):
    user.counter(cpu)
    strike_alert(False, True, cpu)
  else:
    parry_alert(True, True, cpu)
    counter_alert(True, user)
    if not user.parry(cpu):
      cpu.counter(user)
      parry_alert(False, False, user)
    else:
      parry_alert(False, True, user)
      counter_alert(False, cpu)
      user.counter(cpu)
      strike_alert(False, True, cpu)

def cpu_counter_vs_user_analysis():
  counter_alert(True, user)
  if not user.evade():
    cpu.counter(user)
    evade_alert(False, False, user)
  else:
    evade_alert(False, True, user)
    user_data = user.extract(cpu)
    if not user_data:
      memory_alert(False)
    else:
      database_alert(False, user_data)

def cpu_analysis_vs_user_transfer():
  user_corpse = user.link
  user.transfer(user_scan_select())
  transfer_alert(False, user_corpse, user)
  ambush_alert(False, cpu)
  if not cpu.evade():
    user.ambush(cpu)
    strike_alert(False, True, cpu)
  else:
    evade_alert(True, True, cpu)
    cpu_data = cpu.extract(user)
    if not cpu_data:
      memory_alert(True)
    else:
      database_alert(True, cpu_data)

def cpu_analysis_vs_user_sequence():
  sequence_alert(False, cpu.link)
  cpu_error = False
  for strike in user.sequence():
    if not cpu.link.functional:
      user.strike(cpu)
      strike_alert(False, True, cpu)
    elif not strike:
      strike_alert(False, False, cpu)
    elif not cpu.evade():
      cpu_error = True
      user.strike(cpu)
      strike_alert(False, True, cpu)
    else:
      evade_alert(True, True, cpu)
  if cpu_error is False:
    cpu_data = cpu.extract(user)
    if not cpu_data:
      memory_alert(True)
    else:
      database_alert(True, cpu_data)

def cpu_analysis_vs_user_counter():
  counter_alert(False, cpu)
  if not cpu.evade():
    user.counter(cpu)
    strike_alert(False, True, cpu)
  else:
    evade_alert(True, True, cpu)
    cpu_data = cpu.extract(user)
    if not cpu_data:
      memory_alert(True)
    else:
      database_alert(True, cpu_data)

def cpu_analysis_vs_user_analysis():
  cpu.use_memory()
  cpu_data = cpu.extract(user)
  if not cpu_data:
    memory_alert(True)
  else:
    database_alert(True, cpu_data)
  user.use_memory()
  user_data = user.extract(cpu)
  if not user_data:
    memory_alert(False)
  else:
    database_alert(False, user_data)


versus = {
  (0, 'h'): cpu_transfer_vs_user_transfer, 
  (0, 'j'): cpu_transfer_vs_user_sequence, 
  (0, 'k'): cpu_transfer_vs_user_counter, 
  (0, 'l'): cpu_transfer_vs_user_analysis, 
  (1, 'h'): cpu_sequence_vs_user_transfer, 
  (1, 'j'): cpu_sequence_vs_user_sequence, 
  (1, 'k'): cpu_sequence_vs_user_counter, 
  (1, 'l'): cpu_sequence_vs_user_analysis, 
  (2, 'h'): cpu_counter_vs_user_transfer, 
  (2, 'j'): cpu_counter_vs_user_sequence, 
  (2, 'k'): cpu_counter_vs_user_counter, 
  (2, 'l'): cpu_counter_vs_user_analysis, 
  (3, 'h'): cpu_analysis_vs_user_transfer, 
  (3, 'j'): cpu_analysis_vs_user_sequence, 
  (3, 'k'): cpu_analysis_vs_user_counter, 
  (3, 'l'): cpu_analysis_vs_user_analysis
}

def cpu_scan_select():
  scan = cpu.scan()
  sample = [corpse for corpse in scan if corpse is not user.link]
  return random.choice(sample)

def user_scan_select():
  scan = user.scan()
  index = None
  while index not in range(len(scan)):
    scanner_alert()
    index = scan_select.get(input(scanner(False, scan)))
    clear()
  return scan[index]

def injection_select():
  index = None
  while index not in range(len(grave)):
    stealth_alert()
    index = scan_select.get(input(scanner(False, grave)))
    clear()
  return grave[index]

def network_scanner():
  scanner_alert()
  input(scanner(True, field))
  clear()

def dead_scan():
  for corpse in field[-1::-1]:
    if not corpse.functional:
      corpse.expire()

def live_scan():
  for corpse in grave[-1::-1]:
    corpse.reanimate()

def kill_counter():
  return alert(False, 'KILL COUNT: {}'.format(state.kill_count))

def storage_upgrade():
  storage = user.storage
  user.update(state.capacity)
  read(archive, random.choice(list(archive.keys())))
  storage_alert(storage, user.storage)

def cpu_reset():
  cpu.reset()
  if state.hazard:
    cpu.upgrade(state.capacity + 1)
  else:
    cpu.upgrade(state.capacity)

def kill():
  hazard = state.hazard
  state.kill()
  input(kill_counter() + f'   [ {one_liner().ljust(24, " ")} ]\n')
  if hazard:
    storage_upgrade()
  cpu_reset()
  clear()

def reboot():
  user.reboot()
  user.upgrade(state.capacity)
  system_reboot()
  clear()
  if user.scan():
    user.transfer(user_scan_select())
    transfer_alert(False, None, user)
  else:
    state.cloak()
    user.transfer(cpu.link)
    transfer_alert(False, None, user)
    kill()
    stealth_injection()

def restore():
  state.restore()
  while True:
    revenge = input(restore_backup)
    clear()
    if revenge == 'r':
      reboot()
    elif revenge == 'q':
      quit_confirm()
    else:
      continue

def death():
  for i in range(8):
    critical_error()
  clear()
  if state.backup:
    restore()
  else:
    while True:
      failure = input(not_found)
      clear()
      if failure == 'q':
        quit()
      else:
        continue

def checkpoint():
  if not user.active:
    death()
  else:
    user.synchronize()
  if not cpu.active:
    kill()
  else:
    user.synchronize()

def combat_display(cpu_command):
  return input(kill_counter() + hostile(cpu) + (warning.get(cpu_command) if user.intel else empty) + corpse_head + '\n' + info(user))

def combat_hostile():
  if cpu.link:
    cpu_command = cpu_command_select()
  user_command = None
  while state.alerted or len(field) > 1:
    if not cpu.link and (state.alert or user.scan()):
      hostile_insertion()
      cpu_command = cpu_command_select()
    print(f'[ WAVE {state.wave:<2} | HOST {state.hostile:<2} | ALERT {"!" if state.alerted else "_"} ]')
    user_command = combat_display(cpu_command)
    clear()
    if (user_command == 'h' and user.scan()) or user_command in ['j', 'k', 'l']:
      user.intel = False
      versus[cpu_command, user_command]()
      dead_scan()
      if cpu.active:
        cpu_command = cpu_command_select()
      checkpoint()
      clear()
    elif user_command == ';':
      network_scanner()
    elif user_command == 'q':
      quit_confirm()
    elif user_command == injection:
      view_vital_points()
      clear()
    else:
      continue
  state.cloak()

def code_injection():
  limit = int(16 - numpy.sqrt(cpu.data))
  user.memory = 16
  runtime = 0
  payload = 0
  injection_alert(payload)
  while runtime < limit and not cpu.ice():
    runtime += 1
    payload = int(numpy.clip(payload + user.inject(), 0, 255))
    clear()
    injection_alert(payload)
    if payload == 255:
      return True
  return False
  
def stealth_injection():
  while state.stealth and grave:
    corpse = injection_select()
    stealth = code_injection()
    if stealth and not state.hazard:
      injection_success(corpse)
      continue
    else:
      injection_failure(corpse)
      break
  state.alert()

def injection_success(corpse):
  user_corpse = user.link
  corpse.reanimate()
  user.transfer(corpse)
  transfer_alert(False, user_corpse, user)
  kill()

def injection_failure(corpse):
  state.alert()
  corpse.reanimate()
  cpu.transfer(corpse)
  counter_alert(True, user)
  motion_tracker()
  if state.hazard:
    hazard_alert(cpu)
  clear()

def motion_tracker():
  distance = random.randint(1, 10)
  for meter in range(distance):
    distance -= 1
    clear()
    tracker_alert(cpu.link, distance)

def hostile_insertion():
  if cpu.scan():
    cpu.transfer(cpu_scan_select())
    network_alert(cpu)
  else:
    cpu_corpse = random.choice(grave)
    cpu_corpse.reanimate()
    cpu.transfer(cpu_corpse)
    motion_tracker()
  if state.hazard:
    hazard_alert(cpu)
  clear()

def run_confirm():
  while True:
    confirm = input(infiltrate)
    clear()
    if confirm == 'r':
      return
    else:
      continue

def quit_confirm():
  confirm = input(exfiltrate)
  clear()
  if confirm == 'q':
    quit()
  return

def read_archive():
  for record in archive:
    read(archive, record)

def read_manual():
  for page in manual:
    read(manual, page)

def run():
  play_tape()
  while True:
    rtfm = input('\n\n\n\n\n\n\n[!][ :. READ THE FN MANUAL ? ]\n   [;][ READ ]\n   [r][ NAH ]\n')
    clear()
    if rtfm == ';':
      read_manual()
    elif rtfm == 'r':
      run_confirm()
      break
    else:
      continue

cpu = Pilot()
user = Pilot()

corpse_0 = Corpse()
corpse_1 = Corpse()
corpse_2 = Corpse()
corpse_3 = Corpse()
corpse_4 = Corpse()
corpse_5 = Corpse()

state = State()

corpse_0.reanimate()
user.transfer(corpse_0)
user.link.integrity = 255


def main():
  while True:
    if state.stealth:
      stealth_injection()
    else:
      combat_hostile()

run()
main()