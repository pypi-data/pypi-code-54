

try:
    import readline
except ImportError:
    print(
        '\nOops...\n'
        'The game needs readline. '
        'Please try `pip install readline` or `pip install pyreadline`.'
    )

class ITD_game(object):
    
    _ = None

    def __init__(self):
        super(ITD_game, self).__init__()
        if self.__class__._ is not None:
            raise Exception('Cannot create more than on game')
        self.__class__._ = self

        readline.rl.set_pre_input_hook(self._pre_input)

        self.last_input = None
        self.input_count = 0
        self._won = False
        self.inventory = []

        self.current_stage = None
        self.start_stage(FindIgnitionKeys)

    def _pre_input(self):
        if self.current_stage is None:
            return

        import sys
        if readline.rl.prompt != sys.ps1.encode('ascii'):
            return

        if self._won:
            self.current_stage = None
            self.show_message(
                "---",
                "! Woot Woot !",
                "! YOU'R OUT \o/",
                "!!! CONGRAT !!!",
                "---",
                "Yep, that's all... ",
                "I need to go to sleep now ^_^",
                "---",
            )
            return

        prev_input = readline.rl.get_history_item(0)
        if prev_input != self.last_input:
            self.last_input = prev_input
            self.input_count += 1
            self.current_stage.react(self.last_input)

        self.show_hud()
    
    def beep(self):
        print('\a')

    def show_hud(self):
        msg = [
            f"[In The Dark] #{self.input_count}",
            self.current_stage.title,
            self.current_stage.message,
        ]
        inv = [ item for item in self.inventory if item._ITD_Visible() ]
        if inv:
            msg.extend(
                ['Inventory:']
                +['    '+item.hud() for item in inv ]
            )
        self._show_message(*msg)

    def show_message(self, *lines):
        self.beep()
        self._show_message(*lines)

    def _show_message(self, *lines):
        if lines:
            lines = ("",)+lines

        HR = 60*'-'
        got_HR = False
        for line in lines:
            if line == '---':
                line = HR
                got_HR = True
            elif got_HR:
                line = '| '+str(line)
            print(line)
        if got_HR:
            print()

    def add_to_inventory(self, item):
        globals()['__builtins__'][item.__class__.__name__] = item
        self.inventory.append(item)

    def start_stage(self, StageType):
        stage = StageType(self)
        self.current_stage = stage
        self.current_stage.start()

class ITD_Item(object):

    def __init__(self, in_inventory=True):
        super(ITD_Item, self).__init__()
        self._ITD_game = ITD_game._
        self._ITD_visible = False
        if in_inventory:
            self._ITD_game.add_to_inventory(self)

    def _ITD_Visible(self):
        return self._ITD_visible

    def hud(self):
        return self.__class__.__name__

class ITD_Stage(object):

    def __init__(self, game):
        super(ITD_Stage, self).__init__()
        self.game = game
        self.title = 'Stage title'
        self.message = 'Stage message...'

        self.input_count = 0
        self.hint_frequency = 5
        self.hint_index = 0
        self.hints = [
            "Think ! What's the best thing to do now !?"
        ]

    def start(self):
        print('Stage starting up')

    def react(self, last_input):
        self.input_count += 1
        self.do_hint(force='?' in last_input)

    def do_hint(self, force=False):
        if force or not self.input_count % self.hint_frequency:
            self.print_hint()

    def print_hint(self):
        self.game.show_message(
            "---",
            self.hints[self.hint_index],
            "---"
        )
        self.hint_index = (self.hint_index +1) % len(self.hints)

class IgnitionKey(ITD_Item):

    def __init__(self):
        super(IgnitionKey, self).__init__(in_inventory=False) 
        self._ITD_game.IgnitionKey = self
        self._engine = Engine()
        
        self._ITD_visible = False
        self._engine._ITD_visible = False

    def __repr__(self):
        if not self._ITD_Visible():
            self._ITD_game.add_to_inventory(self)
            self._ITD_visible = True
            self._ITD_game.start_stage(TurnEngineOn)
        return super(IgnitionKey, self).__repr__()

    def turn(self):
        self._ITD_visible = True
        if self._engine.is_on():
            self._engine.turn_off()
        else:
            self._engine.turn_on()

class FindIgnitionKeys(ITD_Stage):

    def __init__(self, game):
        super(FindIgnitionKeys, self).__init__(game)
        self.title = "You're in the dark..."
        self.message = "Let's search what's around here !"
        self.input_count = 0
        self.hints = [
            "Were can you find stuff here ?",
            "What is available here ? Where does it come from ?",
            "Look in you pocket !!!",
            "Find your pocket and list what's inside !!!",
        ]

    def start(self):
        import types, sys
        pocket = types.ModuleType('pocket', 'your combinaison pocket.')
        pocket.IgnitionKey = IgnitionKey()
        sys.modules['pocket'] = pocket
        sys.modules['__main__'].pocket = pocket
        #globals()['__builtins__']['IgnitionKey'] = self.game.IgnitionKey
        self.game.show_message(
            "",
            '---',
            "You just woke up.",
            "Your head hurts.",
            "You're in some sort of cockpit, all systems look down.",
            "---",
        )

class PowerCell(object):

    def __init__(self, engine):
        super(PowerCell, self).__init__()
        self.engine = engine
        self.energy = 10
    
    def consume(self):
        self.energy -= 1

        game = self.engine._ITD_game
        if not self.energy:
            game.show_message(
                "---",
                "One of the engine power cells just ran out of energy :/",
                "You got {} more to go".format(
                    len([p for p in self.engine.power_cells if p.energy])
                ),
                "---",
            )

        trunk = self.engine._ITD_game.Trunk
        for pc in self.engine.power_cells:
            if pc in trunk.content:
                trunk.content.remove(pc)
        self.engine.power_cells = [
            pc for pc in self.engine.power_cells
            if pc.energy
        ]
        if not self.engine.power_cells:
            game.show_message(
                "---",
                "DAMN ! No more power !",
                "Engine is shuting down :/",
                "---",
            )    
            self.engine.turn_off()

class Trunk(ITD_Item):

    def __init__(self, engine):
        super(Trunk, self).__init__()
        self._engine = engine
        self._ITD_game.Trunk = self
        self.content = []
        for i in range(4):
            self.content.append(
                PowerCell(self._ITD_game.Engine)
            )

    def _ITD_Visible(self):
        return self._engine._ITD_Visible()

    def hud(self):
        return '{} [Content: {}]'.format(
            self.__class__.__name__,
            len(self.content)
        )

class Engine(ITD_Item):

    def __init__(self):
        super(Engine, self).__init__()
        self._ITD_game.Engine = self
        self._is_on = False
        self.power_cells = []

        self._dirs = '<^>V'
        self._moves = (
            (-1,0), (0,-1), (1,0), (0,1),
        )
        self._dir = 'V'
        self._pos = [11,4]
        Trunk(self)
            
    def turn(self):
        if not self._is_on:
            return
        i = self._dirs.find(self._dir)
        i += 1
        i = i % len(self._dirs)
        self._dir = self._dirs[i]

    def forward(self):
        if not self._is_on:
            return
        o = self._moves[self._dirs.find(self._dir)]
        new_x = self._pos[0] + o[0]
        new_y = self._pos[1] + o[1]
        at = self._ITD_game.Radar[(new_x, new_y)]
        if at in "X|+-D":
            return
        if at == "P":
            pc = PowerCell(self)
            pc.energy = 20
            self.power_cells.append(pc)
            self._ITD_game.Radar[(new_x, new_y)] = ' '
        elif at == "B":
            self.power_cells.clear()
            import pocket
            pocket.last_power_cells = 4*[PowerCell(self)]
            self._ITD_game.show_message(
                "---",
                "OOOOOOH NOOO !!! You hit a bomb !",
                "Engine looks Ok but all batteries are dead ! :(",
                "Find some more to keep exploring...",
                "---",
            )
            self._ITD_game.Radar[(new_x, new_y)] = ' '
        elif at == 'K':
            m = self._ITD_game.Radar._ITD_map
            nm = []
            for row in m:
                nm.append(row.replace('D', ' '))
            self._ITD_game.Radar._ITD_map = nm
            self._ITD_game.Radar[(new_x, new_y)] = ' '
        elif at == 'O':
            self._ITD_game._won = True
        self._pos = (new_x, new_y)

    def is_on(self):
        return self._is_on

    def turn_on(self):
        self._ITD_visible = True
        if not self._ITD_game.IgnitionKey._ITD_Visible():
            self._ITD_game.show_message(
                "---", 
                "Hmmm... I think you need a key to turn this on...",
                "---"
            )
            return
        if not self.power_cells:
            self._ITD_game.show_message(
                "---", 
                "Battery is out, I need to find some energy cells !",
                "---"
            )
            return
        self._is_on = True
        self._ITD_game.start_stage(UseTheRadar)
        globals()['__builtins__']['t'] = self.turn
        globals()['__builtins__']['f'] = self.forward
   
    def turn_off(self):
        self._ITD_visible = True
        if not self._is_on:
            return
        self._is_on = False
        self._ITD_game.start_stage(TurnEngineOn)
    
    def hud(self):
        if self._is_on and self.power_cells:
            self.power_cells[-1].consume()
        return '{} [{}] [Power:{}]'.format(
            self.__class__.__name__,
            self._is_on and "ON" or "OFF",
            ', '.join([str(p.energy) for p in self.power_cells]) or 'XXX'
        )
        
class TurnEngineOn(ITD_Stage):

    def __init__(self, game):
        super(TurnEngineOn, self).__init__(game)
        self.title = "You're in the dark..."
        self.message = "Turn the engin on !"
        self.powerless_hints = [
            "Boy, you're strungling ^.^",
            "Maybe look in the trunk ?",
        ]
        self.powered_hints = [
            "No that you have power, turn the engine on !",
        ]
        self.hints = self.powerless_hints

    def start(self):
        if self.game.Engine._ITD_Visible():
            self.game.show_message(
                "---",
                "We need to get this Engin on !",
                "---",
            )
        else:
            self.game.show_message(
                "---",
                "Look, there is an IgnitionKey there !",
                "Let's use it :)",
                "---",
            )

    def react(self, *args, **kwargs):
        if self.game.Engine.power_cells:
            self.hints = self.powered_hints
            self.game.show_message(
                "---",
                "Nice ! You reloaded the Engine batteries !",
                "---",
                "Now turn the Engine on !",
                "---",
            )
        super(TurnEngineOn, self).react(*args, **kwargs)

class Radar(ITD_Item):

    def __init__(self):
        super(Radar, self).__init__()
        self._ITD_game.Radar = self
        self._ITD_visible = True
        self._ITD_map = [
            'P       |          O',
            '----    D B         ',
            '        |     ------',
            ' B  ----+---+       ',
            '            | ------',
            '----- P |   |       ',
            '        | B +------ ',
            '   |                ',
            '   +-------------   ',
            ' K |  P P P         ',
        ]
    
    def __getitem__(self, pos):
        try:
            x, y = pos
        except Exception:
            return None
        return self._ITD_map[y][x]

    def __setitem__(self, pos, c):
        try:
            x, y = pos
        except Exception:
            return

        row = self._ITD_map[y]
        row = row[:x]+c+row[x+1:]
        self._ITD_map[y] = row

    def hud(self):
        if not self._ITD_game.Engine._is_on:
            return '{} [OFF]'.format(self.__class__.__name__)

        # map w and h
        mw = 20
        mh = 10

        engine = self._ITD_game.Engine

        import math
        w = len(engine.power_cells)*2+1
        wo = math.ceil(w/2)
        h = math.ceil(w/2)
        ho = math.ceil(h/2)
        offsets = []
        for y in range(1, h+1):
            line = []
            offsets.append(line)
            for x in range(1, w+1):
                line.append(((x-wo),y-ho))

        x = engine._pos[0]
        y = engine._pos[1]
        view = []
        idt = 8*' '
        view += idt+'+'+w*'-'+'+\n'
        for line_offsets in offsets:
            view += idt+'|'
            for offset in line_offsets:
                vx = x+offset[0]
                vy = y+offset[1]
                if vx >= mw or vy >= mh or vx < 0 or vy < 0:
                    view += 'X'
                else:
                    view += self._ITD_map[vy][vx]
                if not offset[0] and not offset[1]:
                    view[-1:] = engine._dir
            view += '|\n'
        view += idt+'+'+w*'-'+'+\n'
        return '{}:\n{}'.format(
            self.__class__.__name__,
            ''.join(view)
        )
            

class UseTheRadar(ITD_Stage):

    def __init__(self, game):
        super(UseTheRadar, self).__init__(game)
        self.title = "Screen is showing data."
        self.message = "Is it a radar or something ?"
    
    def start(self):
        try:
            self.engine.Radar
        except:
            Radar()
        
        self.game.show_message(
            "---",
            "Alright ! Engine is ON \o/",
            "(You can turn with `t()` and move forward with `f()`)",
            "---"
        )

ITD_game()
'''
import itd
import importlib
importlib.reload(itd)
Engine.power_cells.extend(Trunk.content)
IgnitionKey.turn()
'''