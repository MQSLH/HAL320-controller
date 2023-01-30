from dataclasses import dataclass, field

@dataclass
class HAL320:
    """A class to store the current lamp state"""
    window: 'typing.Any' = field(init=False, repr=False) 
    _shutterOpen: bool
    _timer: float
    _intensity: int
    _lampOn: bool
    _life: float
    _version: str 

    @property
    def shutterOpen(self) -> bool:
        return self._shutterOpen
    @shutterOpen.setter
    def shutterOpen(self, v: bool) -> None:
        self._shutterOpen = v        
        if hasattr(self, 'window'):
            if v:
                self.window.btn_shutter.configure(bg ='green')
            else:
                self.window.btn_shutter.configure(bg ='red')

    @property
    def timer(self) -> float:
        return self._timer
    @timer.setter
    def timer(self, v: float) -> None:
        self._timer = v

    @property
    def intensity(self) -> int:
        return self._intensity
    @intensity.setter
    def intensity(self, v: int) -> None:
        self._intensity = v  

    @property
    def lampOn(self) -> bool:
        return self._lampOn
    @lampOn.setter
    def lampOn(self, v: bool) -> None:
        self._lampOn = v
        if hasattr(self, 'window'):
            if v:
                self.window.btn_power.configure(bg ='green')
            else:
                self.window.btn_power.configure(bg ='red')

    @property
    def life(self) -> float:
        return self._life
    @life.setter
    def life(self, v: float) -> None:
        self._life = v        

    @property
    def version(self) -> str:
        return self._version
    @version.setter
    def version(self, v: float) -> None:
        self._version = v 