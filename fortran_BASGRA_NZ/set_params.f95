Subroutine set_params(pa)

use parameters_site
use parameters_plant

implicit none

real      :: pa(NPAR) !npar set in parameters_site

! a script checks that these variable names match what is expected in the parameter.txt file (Simon)
! Initial values
LOG10CLVI  = pa(1)
LOG10CRESI = pa(2)
LOG10CRTI  = pa(3)
CSTI	   = pa(4)
LOG10LAII  = pa(5)
PHENI	   = pa(6)
TILTOTI	   = pa(7)
FRTILGI	   = pa(8)
LT50I      = pa(9)

! Process parameters
CLAIV     = pa(10)
COCRESMX  =	pa(11)
CSTAVM	  = pa(12)
DAYLB	  =	pa(13)
DAYLP	  =	pa(14)
DLMXGE	  = pa(15)
FSLAMIN   = pa(16)
FSMAX     = pa(17)
HAGERE    =	pa(18)
KLAI      =	pa(19)
LAICR	  = pa(20)
LAIEFT    = pa(21)
LAITIL	  =	pa(22)
LFWIDG	  =	pa(23)
LFWIDV	  = pa(24)
NELLVM	  = pa(25)
PHENCR    = pa(26)
PHY	      =	pa(27)
RDRSCO	  =	pa(28)
RDRSMX	  = pa(29)
RDRTEM    = pa(30)
RGENMX	  =	pa(31)
ROOTDM	  =	pa(32)
RRDMAX	  = pa(33)
RUBISC    = pa(34)
LSHAPE	  =	pa(35)
SIMAX1T	  =	pa(36)
SLAMAX    = pa(37)
TBASE     = pa(38)
TCRES     = pa(39)
TOPTGE	  =	pa(40)
TRANCO	  = pa(41)
YG        = pa(42)

LAT       = pa(43)
WCI       = pa(44)
FWCAD     = pa(45)
FWCWP     = pa(46)
FWCFC     = pa(47)
FWCWET    = pa(48)
WCST      = pa(49)
WpoolMax  = pa(50)

Dparam	     = pa(51)
FGAS	     = pa(52)
FO2MX	     = pa(53)
KTSNOW	     = pa(54)
Hparam	     = pa(55)
KRDRANAER    = pa(56)
KRESPHARD    = pa(57)
KRSR3H	     = pa(58)
KRTOTAER     = pa(59)
KSNOW	     = pa(60)
LAMBDAsoil   = pa(61)
LDT50A	     = pa(62)
LDT50B	     = pa(63)
LT50MN	     = pa(64)
LT50MX	     = pa(65)
RATEDMX	     = pa(66)
reHardRedDay = pa(67)
RHOnewSnow	 = pa(68)
RHOpack	     = pa(69)
SWret	     = pa(70)
SWrf	     = pa(71)
THARDMX	     = pa(72)
TmeltFreeze	 = pa(73)
TrainSnow	 = pa(74)
TsurfDiff	 = pa(75)
KLUETILG	 = pa(76)
FRTILGG1I	 = pa(77)
DAYLG1G2     = pa(78)
RGRTG1G2     = pa(79)
RDRTMIN      = pa(80)
TVERN        = pa(81)
TVERND       = pa(82)
RDRSTUB      = pa(83)
LERGB        = pa(84)
RDRROOT      = pa(85)
DAYLA        = pa(86)
DAYLRV       = pa(87)
FCOCRESMN    = pa(88)
KCRT         = pa(89)
VERNDI       = pa(90)
LERVA        = pa(91)
LERVB        = pa(92)
LERGA        = pa(93)
RDRTILMIN    = pa(94)
RDRHARVMAX   = pa(95)
FGRESSI      = pa(96)
BD           = pa(97)
HARVFRD      = pa(98)
EBIOMAX      = pa(99)
KBASAL       = pa(100)
RDRWMAX      = pa(101)
BASALI       = pa(102)
ABASAL       = pa(103)
TVERNDMN     = pa(104)
DAYLGEMN     = pa(105)
TRANRFCR     = pa(106)
DELE         = pa(107)
DELD         = pa(108)

! previous site parameters brough out of the model
IRRIGF       = pa(109)
DRATE        = pa(110) ! mm d-1 Maximum soil drainage rate !
CO2A         = pa(111)
poolInfilLimit = pa(112)

! new irrigation parameters

if (pa(113) < 0.9) then ! sudo boolean as float, expects 1 or 0
    Irr_frm_PAW  = .FALSE.
else
    Irr_frm_PAW = .TRUE.
end if

! new harvest parameters

if (pa(114) < 0.9) then ! sudo boolean as float, expects 1 or 0
    FIXED_REMOVAL = .FALSE.
else
    FIXED_REMOVAL = .TRUE.
end if
if (pa(115) < 0.9) then ! sudo boolean as float, expects 1 or 0
    opt_harvfrin = .FALSE.
else
    opt_harvfrin = .TRUE.
end if

! reseed parameters
reseed_harv_delay  =  INT(pa(116))  ! number of days to delay harvest after reseed, must be >=1
reseed_LAI         = pa(117)  ! >=0 the leaf area index to set after reseeding, if < 0 then simply use the current LAI
reseed_TILG2       = pa(118)  ! Non-elongating generative tiller density after reseed if >=0 otherwise use current state of variable
reseed_TILG1       = pa(119)  ! Elongating generative tiller density after reseed if >=0 otherwise use current state of variable
reseed_TILV        = pa(120)  ! Non-elongating tiller density after reseed if >=0 otherwise use current state of variable
reseed_CLV         = pa(121)
reseed_CRES        = pa(122)
reseed_CST         = pa(123)
reseed_CSTUB       = pa(124)

return
end
