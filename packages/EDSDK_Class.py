# MIT License

# Copyright (c) 2023 [Philippe Lopez]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Property:
#  Camera Setting Properties
	Unknown                = 0x0000ffff
	ProductName            = 0x00000002
	OwnerName              = 0x00000004
	MakerName              = 0x00000005
	DateTime               = 0x00000006
	FirmwareVersion        = 0x00000007
	BatteryLevel           = 0x00000008
	SaveTo                 = 0x0000000b
	CurrentStorage         = 0x0000000c
	CurrentFolder          = 0x0000000d
	BatteryQuality         = 0x00000010	
	BodyIDEx			   = 0x00000015
	HDDirectoryStructure   = 0x00000020	
	TempStatus             = 0x01000415

	SaveTo_Camera          = 1
	SaveTo_Host            = 2
	SaveTo_Both            = SaveTo_Camera | SaveTo_Host

#  Image Properties
	ImageQuality           = 0x00000100
	Orientation            = 0x00000102
	ICCProfile             = 0x00000103
	FocusInfo              = 0x00000104
	WhiteBalance           = 0x00000106
	ColorTemperature       = 0x00000107
	WhiteBalanceShift      = 0x00000108
	ColorSpace             = 0x0000010d
	PictureStyle           = 0x00000114
	PictureStyleDesc       = 0x00000115
	PictureStyleCaption    = 0x00000200

#  Image GPS Properties
	GPSVersionID		   = 0x00000800 	
	GPSLatitudeRef		   = 0x00000801 		
	GPSLatitude			   = 0x00000802 	
	GPSLongitudeRef		   = 0x00000803 	
	GPSLongitude		   = 0x00000804 		
	GPSAltitudeRef		   = 0x00000805 		
	GPSAltitude			   = 0x00000806 		
	GPSTimeStamp		   = 0x00000807 		
	GPSSatellites		   = 0x00000808 		
	GPSStatus			   = 0x00000809
	GPSMapDatum			   = 0x00000812 		
	GPSDateStamp		   = 0x0000081D 		

#  Capture Properties
	AEMode                 = 0x00000400
	DriveMode              = 0x00000401
	ISOSpeed               = 0x00000402
	MeteringMode           = 0x00000403
	AFMode                 = 0x00000404
	Av                     = 0x00000405
	Tv                     = 0x00000406
	ExposureCompensation   = 0x00000407
	FocalLength            = 0x00000409
	AvailableShots         = 0x0000040a
	Bracket                = 0x0000040b
	WhiteBalanceBracket    = 0x0000040c
	LensName               = 0x0000040d
	AEBracket              = 0x0000040e
	FEBracket              = 0x0000040f
	ISOBracket             = 0x00000410
	NoiseReduction         = 0x00000411
	FlashOn                = 0x00000412
	RedEye                 = 0x00000413
	FlashMode              = 0x00000414
	LensStatus             = 0x00000416
	Artist	               = 0x00000418
	Copyright	           = 0x00000419
	AEModeSelect           = 0x00000436
	PowerZoom_Speed		   = 0x00000444

#  EVF Properties
	Evf_OutputDevice        = 0x00000500
	Evf_Mode                = 0x00000501
	Evf_WhiteBalance        = 0x00000502
	Evf_ColorTemperature    = 0x00000503
	Evf_DepthOfFieldPreview = 0x00000504

#  EVF IMAGE DATA Properties
	Evf_Zoom                = 0x00000507
	Evf_ZoomPosition        = 0x00000508
	Evf_Histogram           = 0x0000050A
	Evf_ImagePosition       = 0x0000050B
	Evf_HistogramStatus     = 0x0000050C
	Evf_AFMode              = 0x0000050E

	Record                  = 0x00000510

	Evf_HistogramY          = 0x00000515
	Evf_HistogramR          = 0x00000516
	Evf_HistogramG          = 0x00000517
	Evf_HistogramB          = 0x00000518

	Evf_CoordinateSystem    = 0x00000540
	Evf_ZoomRect            = 0x00000541
	Evf_ImageClipRect       = 0x00000545

	Evf_PowerZoom_CurPosition = 0x00000550
	Evf_PowerZoom_MaxPosition = 0x00000551
	Evf_PowerZoom_MinPosition = 0x00000552

# Limited Properties
	UTCTime                 = 0x01000016
	TimeZone                = 0x01000017
	SummerTimeSetting       = 0x01000018
	ManualWhiteBalanceData  = 0x01000204
	MirrorLockUpState       = 0x01000421
	FixedMovie              = 0x01000422
	MovieParam              = 0x01000423
	Aspect                  = 0x01000431
	MirrorUpSetting         = 0x01000438
	MovieServoAf            = 0x0100043e
	AutoPowerOffSetting     = 0x0100045e
	AFEyeDetect             = 0x01000455
	Evf_ClickWBCoeffs       = 0x01000506
	EVF_RollingPitching     = 0x01000544
	Evf_VisibleRect         = 0x01000546
	StillMovieDivideSetting = 0x01000470
	CardExtension           = 0x01000471
	MovieCardExtension      = 0x01000472
	StillCurrentMedia       = 0x01000473
	MovieCurrentMedia       = 0x01000474
	FocusShiftSetting       = 0x01000457
	MovieHFRSetting         = 0x0100045d

#  DC Properties
	DC_Zoom                	= 0x00000600
	DC_Strobe               = 0x00000601
	LensBarrelStatus		= 0x00000605

class Command:
	# Camera commands
	# -----------------------------------------------------------------------------
	# 	Send Commands
	# -----------------------------------------------------------------------------
	TakePicture                     = 0x00000000       
	ExtendShutDownTimer             = 0x00000001
	BulbStart			            = 0x00000002 
	BulbEnd				            = 0x00000003 
	DoEvfAf                         = 0x00000102
	DriveLensEvf                    = 0x00000103,
	DoClickWBEvf                    = 0x00000104
	MovieSelectSwON                 = 0x00000107
	MovieSelectSwOFF                = 0x00000108 

	PressShutterButton              = 0x00000004
	SetRemoteShootingMode           = 0x0000010f
	RequestRollPitchLevel           = 0x00000109
	RequestSensorCleaning           = 0x00000112
	SetModeDialDisable              = 0x00000113

	ShutterButton_OFF				= 0x00000000
	ShutterButton_Halfway			= 0x00000001
	ShutterButton_Completely		= 0x00000003
	ShutterButton_Halfway_NonAF		= 0x00010001
	ShutterButton_Completely_NonAF	= 0x00010003

class DriveMode:
	Value = {
		"Single shooting":              0x00,
		"Medium speed continuous":      0x01, 
		"High speed continuous":        0x04, 
		"Low speed continuous":         0x05, 
		"Single Silent(Soft) shooting": 0x06, 
		"Self-timer:Continuous":        0x07, 
		"Self-timer 10 sec":            0x10, 
		"Self-timer 2 sec":             0x11, 
		"High speed continuous +":      0x12, 
		"Silent single shooting":       0x13, 
		"Silent(Soft) contin shooting": 0x14, 
		"Silent HS continuous":         0x15, 
		"Silent(Soft) LS continuous":   0x16 
	}

class AEMode:
	Program              = 0x00 
	Tv                   = 0x01
	Av                   = 0x02
	Manual               = 0x03
	Bulb                 = 0x04
	A_DEP                = 0x05
	DEP                  = 0x06
	Custom               = 0x07
	Lock                 = 0x08
	Green                = 0x09
	NightPortrait        = 0x0A
	Sports               = 0x0B
	Portrait             = 0x0C
	Landscape            = 0x0D
	Closeup              = 0x0E
	FlashOff             = 0x0F
	CreativeAuto         = 0x13
	Movie		  	     = 0x14
	PhotoInMovie		 = 0x15
	SceneIntelligentAuto = 0x16
	SCN                  = 0x19
	NightScenes          = 0x17
	BacklitScenes        = 0x18
	Children             = 0x1A
	Food                 = 0x1B
	CandlelightPortraits = 0x1C
	CreativeFilter       = 0x1D
	RoughMonoChrome      = 0x1E
	SoftFocus            = 0x1F
	ToyCamera            = 0x20
	Fisheye              = 0x21
	WaterColor           = 0x22
	Miniature            = 0x23
	Hdr_Standard         = 0x24
	Hdr_Vivid            = 0x25
	Hdr_Bold             = 0x26
	Hdr_Embossed         = 0x27
	Movie_Fantasy        = 0x28
	Movie_Old            = 0x29
	Movie_Memory         = 0x2A
	Movie_DirectMono     = 0x2B
	Movie_Mini           = 0x2C
	PanningAssist        = 0x2D
	GroupPhoto           = 0x2E
	Myself               = 0x32
	PlusMovieAuto        = 0x33
	SmoothSkin           = 0x34
	Panorama			 = 0x35
	Silent         	     = 0x36
	Flexible             = 0x37
	OilPainting		     = 0x38
	Fireworks		     = 0x39
	StarPortrait		 = 0x3A
	StarNightscape	     = 0x3B
	StarTrails		     = 0x3C
	StarTimelapseMovie   = 0x3D
	BackgroundBlur	     = 0x3E
	VideoBlog            = 0x3F	

class ISO:
	# Map of value and display name
	Value = {
		"Auto"  : 0x00,
		"6"     : 0x28,
		"12"    : 0x30,
		"25"    : 0x38,
		"50"    : 0x40,
		"100"   : 0x48,
		"125"   : 0x4b,
		"160"   : 0x4d,
		"200"   : 0x50,
		"250"   : 0x53,
		"320"   : 0x55,
		"400"   : 0x58,
		"500"   : 0x5b,
		"640"   : 0x5d,
		"800"   : 0x60,
		"1000"  : 0x63,
		"1250"  : 0x65,
		"1600"  : 0x68,
		"2000"  : 0x6b,
		"2500"  : 0x6d,
		"3200"  : 0x70,
		"4000"  : 0x73,
		"5000"  : 0x75,
		"6400"  : 0x78,
		"8000"  : 0x7b,
		"10000" : 0x7d,
		"12800" : 0x80,
		"16000" : 0x83,
		"20000" : 0x85,
		"25600" : 0x88,
		"32000" : 0x8b,
		"40000" : 0x8d,
		"51200" : 0x90,
		"64000" : 0x93,
		"80000" : 0x95,
		"102400": 0x98,
		"204800": 0xa0,
		"409600": 0xa8,
		"819200": 0xb0
		}

class Av:
	# Map of value and display name
	Value = {
		"00"  : 0x00,
		"1"   : 0x08,
		"1.1" : 0x0B,
		# "1.2" : 0x0C,
		"1.2" : 0x0D,
		"1.4" : 0x10,
		"1.6" : 0x13,
		# "1.8" : 0x14,
		"1.8" : 0x15,
		"2"   : 0x18, #
		"2.2" : 0x1B,
		"2.5h" : 0x1C, # 
		"2.5" : 0x1D,
		"2.8" : 0x20, # 
		"3.2" : 0x23,
		"3.5h" : 0x24, #
		"3.5" : 0x25,
		"4"   : 0x28, # 
		"4.5" : 0x2B,
		"4.5h" : 0x2C, #
		"5.0" : 0x2D,
		"5.6" : 0x30, #
		"6.3" : 0x33,
		"6.7" : 0x34, # 1/2
		"7.1" : 0x35,
		"8"   : 0x38, #
		"9"   : 0x3B,
		"9.5" : 0x3C, # 1/2
		"10"  : 0x3D,
		"11"  : 0x40, #
		"13"  : 0x43,
		"13h"  : 0x44, # 1/2
		"14"  : 0x45, 
		"16"  : 0x48, #
		"18"  : 0x4B,
		"19"  : 0x4C, # 1/2
		"20"  : 0x4D,
		"22"  : 0x50, #
		"25"  : 0x53,
		"27"  : 0x54,
		"29"  : 0x55,
		"32"  : 0x58,
		"36"  : 0x5B,
		"38"  : 0x5C,
		"40"  : 0x5D,
		"45"  : 0x60,
		"51"  : 0x63,
		"54"  : 0x64,
		"57"  : 0x65,
		"64"  : 0x68,
		"72"  : 0x6B,
		"76"  : 0x6C,
		"80"  : 0x6D,
		"91"  : 0x70,
		"Auto": 0xFF
		}
	 
class Tv:
	# Map of value and display name
	Value = {
		"Auto"  : 0x04,
		"Bulb"  : 0x0c,
		"30"    : 0x10, #
		"25"    : 0x13,
		"20h"    : 0x14, # 1/2
		"20"    : 0x15,
		"15"    : 0x18, #
		"13"    : 0x1B,
		"10h"    : 0x1C, #
		"10"    : 0x1D,
		"8"     : 0x20, #
		"6"     : 0x23,
		"6h"     : 0x24, #
		"5"     : 0x25,
		"4"     : 0x28, #
		"3.2"   : 0x2B,
		"3"     : 0x2C, # 1/2
		"2.5"   : 0x2D,
		"2"     : 0x30, #
		"1.6"   : 0x33,
		"1.5"   : 0x34, # 1/2
		"1.3"   : 0x35,
		"1"     : 0x38, #
		"0.8"   : 0x3B,
		"0.7"   : 0x3C, # 1/2
		"0.6"   : 0x3D,
		"0.5"   : 0x40, #
		"0.4"   : 0x43,
		"0.3h"   : 0x44, #
		"0.3"   : 0x45,
		"1/4"   : 0x48, #
		"1/5"   : 0x4B, 
		"1/6h"   : 0x4C, #
		"1/6"   : 0x4D,
		"1/8"   : 0x50, #
		"1/10"  : 0x53,
		"1/10h"  : 0x54, #
		"1/13"  : 0x55,
		"1/15"  : 0x58, #
		"1/20"  : 0x5B,
		"1/20h"  : 0x5C, #
		"1/25"  : 0x5D,
		"1/30"  : 0x60, #
		"1/40"  : 0x63,
		"1/45"  : 0x64, # 1/2
		"1/50"  : 0x65,
		"1/60"  : 0x68, #
		"1/80"  : 0x6B,
		"1/90"  : 0x6C, # 1/2
		"1/100" : 0x6D,
		"1/125" : 0x70, #
		"1/160" : 0x73,
		"1/180" : 0x74, # 1/2
		"1/200" : 0x75,
		"1/250" : 0x78, #
		"1/320" : 0x7B,
		"1/350" : 0x7C, # 1/2
		"1/400" : 0x7D,
		"1/500" : 0x80, #
		"1/640" : 0x83,
		"1/750" : 0x84, # 1/2
		"1/800" : 0x85,
		"1/1000": 0x88, #
		"1/1250": 0x8B,
		"1/1500": 0x8C, # 1/2
		"1/1600": 0x8D,
		"1/2000": 0x90, #
		"1/2500": 0x93,
		"1/3000": 0x94, # 1/2
		"1/3200": 0x95,
		"1/4000": 0x98, #
		"1/5000": 0x9B,
		"1/6000": 0x9C, # 1/2
		"1/6400": 0x9D,
		"1/8000": 0xA0  #
	}
	
class Error:
	#  Definition of error Codes
	Get = {
		# ED-SDK Error Code Masks
		0x80000000: "EDS_ISSPECIFIC_MASK",
		0x7F000000: "EDS_COMPONENTID_MASK",
		0x00FF0000: "EDS_RESERVED_MASK",
		0x0000FFFF: "EDS_ERRORID_MASK",

		# ED-SDK Base Component IDs
		0x01000000: "EDS_CMP_ID_CLIENT_COMPONENTID",
		0x02000000: "EDS_CMP_ID_LLSDK_COMPONENTID",
		0x03000000: "EDS_CMP_ID_HLSDK_COMPONENTID",

		# ED-SDK Functin Success Code
		0x00000000: "OK",

		# ED-SDK Generic Error IDs
		# * Miscellaneous errors *
		0x00000001: "UNIMPLEMENTED",
		0x00000002: "INTERNAL_ERROR",
		0x00000003: "MEM_ALLOC_FAILED",
		0x00000004: "MEM_FREE_FAILED",
		0x00000005: "OPERATION_CANCELLED",
		0x00000006: "INCOMPATIBLE_VERSION",
		0x00000007: "NOT_SUPPORTED",
		0x00000008: "UNEXPECTED_EXCEPTION",
		0x00000009: "PROTECTION_VIOLATION",
		0x0000000A: "MISSING_SUBCOMPONENT",
		0x0000000B: "SELECTION_UNAVAILABLE",

		# * File errors *
		0x00000020: "FILE_IO_ERROR",
		0x00000021: "FILE_TOO_MANY_OPEN",
		0x00000022: "FILE_NOT_FOUND",
		0x00000023: "FILE_OPEN_ERROR",
		0x00000024: "FILE_CLOSE_ERROR",
		0x00000025: "FILE_SEEK_ERROR",
		0x00000026: "FILE_TELL_ERROR",
		0x00000027: "FILE_READ_ERROR",
		0x00000028: "FILE_WRITE_ERROR",
		0x00000029: "FILE_PERMISSION_ERROR",
		0x0000002A: "FILE_DISK_FULL_ERROR",
		0x0000002B: "FILE_ALREADY_EXISTS",
		0x0000002C: "FILE_FORMAT_UNRECOGNIZED",
		0x0000002D: "FILE_DATA_CORRUPT",
		0x0000002E: "FILE_NAMING_NA",

		# * Directory errors *
		0x00000040: "DIR_NOT_FOUND",
		0x00000041: "DIR_IO_ERROR",
		0x00000042: "DIR_ENTRY_NOT_FOUND",
		0x00000043: "DIR_ENTRY_EXISTS",
		0x00000044: "DIR_NOT_EMPTY",

		# * Property errors *
		0x00000050: "PROPERTIES_UNAVAILABLE",
		0x00000051: "PROPERTIES_MISMATCH",
		0x00000053: "PROPERTIES_NOT_LOADED",

		# * Function Parameter errors *
		0x00000060: "INVALID_PARAMETER",
		0x00000061: "INVALID_HANDLE",
		0x00000062: "INVALID_POINTER",
		0x00000063: "INVALID_INDEX",
		0x00000064: "INVALID_LENGTH",
		0x00000065: "INVALID_FN_POINTER",
		0x00000066: "INVALID_SORT_FN",

		# * Device errors *
		0x00000080: "DEVICE_NOT_FOUND",
		0x00000081: "DEVICE_BUSY",
		0x00000082: "DEVICE_INVALID",
		0x00000083: "DEVICE_EMERGENCY",
		0x00000084: "DEVICE_MEMORY_FULL",
		0x00000085: "DEVICE_INTERNAL_ERROR",
		0x00000086: "DEVICE_INVALID_PARAMETER",
		0x00000087: "DEVICE_NO_DISK",
		0x00000088: "DEVICE_DISK_ERROR",
		0x00000089: "DEVICE_CF_GATE_CHANGED",
		0x0000008A: "DEVICE_DIAL_CHANGED",
		0x0000008B: "DEVICE_NOT_INSTALLED",
		0x0000008C: "DEVICE_STAY_AWAKE",
		0x0000008D: "DEVICE_NOT_RELEASED",

		# * Stream errors *
		0x000000A0: "STREAM_IO_ERROR",
		0x000000A1: "STREAM_NOT_OPEN",
		0x000000A2: "STREAM_ALREADY_OPEN",
		0x000000A3: "STREAM_OPEN_ERROR",
		0x000000A4: "STREAM_CLOSE_ERROR",
		0x000000A5: "STREAM_SEEK_ERROR",
		0x000000A6: "STREAM_TELL_ERROR",
		0x000000A7: "STREAM_READ_ERROR",
		0x000000A8: "STREAM_WRITE_ERROR",
		0x000000A9: "STREAM_PERMISSION_ERROR",
		0x000000AA: "STREAM_COULDNT_BEGIN_THREAD",
		0x000000AB: "STREAM_BAD_OPTIONS",
		0x000000AC: "STREAM_END_OF_STREAM",

		# * Communications errors *
		0x000000C0: "COMM_PORT_IS_IN_USE",
		0x000000C1: "COMM_DISCONNECTED",
		0x000000C2: "COMM_DEVICE_INCOMPATIBLE",
		0x000000C3: "COMM_BUFFER_FULL",
		0x000000C4: "COMM_USB_BUS_ERR",

		# * Lock/Unlock *
		0x000000D0: "USB_DEVICE_LOCK_ERROR",
		0x000000D1: "USB_DEVICE_UNLOCK_ERROR",

		# * STI/WIA *
		0x000000E0: "STI_UNKNOWN_ERROR",
		0x000000E1: "STI_INTERNAL_ERROR",
		0x000000E2: "STI_DEVICE_CREATE_ERROR",
		0x000000E3: "STI_DEVICE_RELEASE_ERROR",
		0x000000E4: "DEVICE_NOT_LAUNCHED",
		
		0x000000F0: "ENUM_NA",
		0x000000F1: "INVALID_FN_CALL",
		0x000000F2: "HANDLE_NOT_FOUND",
		0x000000F3: "INVALID_ID",
		0x000000F4: "WAIT_TIMEOUT_ERROR",

		# * PTP *
		0x00002003: "SESSION_NOT_OPEN",
		0x00002004: "INVALID_TRANSACTIONID",
		0x00002007: "INCOMPLETE_TRANSFER",
		0x00002008: "INVALID_STRAGEID",
		0x0000200A: "DEVICEPROP_NOT_SUPPORTED",
		0x0000200B: "INVALID_OBJECTFORMATCODE",
		0x00002011: "SELF_TEST_FAILED",
		0x00002012: "PARTIAL_DELETION",
		0x00002014: "SPECIFICATION_BY_FORMAT_UNSUPPORTED",
		0x00002015: "NO_VALID_OBJECTINFO",
		0x00002016: "INVALID_CODE_FORMAT",
		0x00002017: "UNKNOWN_VENDOR_CODE",
		0x00002018: "CAPTURE_ALREADY_TERMINATED",
		0x00002019: "PTP_DEVICE_BUSY",
		0x0000201A: "INVALID_PARENTOBJECT",
		0x0000201B: "INVALID_DEVICEPROP_FORMAT",
		0x0000201C: "INVALID_DEVICEPROP_VALUE",
		0x0000201E: "SESSION_ALREADY_OPEN",
		0x0000201F: "TRANSACTION_CANCELLED",
		0x00002020: "SPECIFICATION_OF_DESTINATION_UNSUPPORTED",
		0x00002021: "NOT_CAMERA_SUPPORT_SDK_VERSION",

		# * PTP Vendor *
		0x0000A001: "UNKNOWN_COMMAND",
		0x0000A005: "OPERATION_REFUSED",
		0x0000A006: "LENS_COVER_CLOSE",
		0x0000A101: "LOW_BATTERY",
		0x0000A102: "OBJECT_NOTREADY",
		0x0000A104: "CANNOT_MAKE_OBJECT",
		0x0000A106: "MEMORYSTATUS_NOTREADY",

		# * Take Picture errors * 
		0x00008D01: "TAKE_PICTURE_AF_NG",
		0x00008D02: "TAKE_PICTURE_RESERVED",
		0x00008D03: "TAKE_PICTURE_MIRROR_UP_NG",
		0x00008D04: "TAKE_PICTURE_SENSOR_CLEANING_NG",
		0x00008D05: "TAKE_PICTURE_SILENCE_NG",
		0x00008D06: "TAKE_PICTURE_NO_CARD_NG",
		0x00008D07: "TAKE_PICTURE_CARD_NG",
		0x00008D08: "TAKE_PICTURE_CARD_PROTECT_NG",
		0x00008D09: "TAKE_PICTURE_MOVIE_CROP_NG",
		0x00008D0A: "TAKE_PICTURE_STROBO_CHARGE_NG",
		0x00008D0B: "TAKE_PICTURE_NO_LENS_NG",
		0x00008D0C: "TAKE_PICTURE_SPECIAL_MOVIE_MODE_NG",
		0x00008D0D: "TAKE_PICTURE_LV_REL_PROHIBIT_MODE_NG",
		0x00008D0E: "TAKE_PICTURE_MOVIE_MODE_NG",
		0x00008D0F: "TAKE_PICTURE_RETRUCTED_LENS_NG",


		0x000000F5: "LAST_GENERIC_ERROR_PLUS_ONE"
	}

class StateEvent:
#  Notifies all state events. 
	All						= 0x00000300
        
#  Indicates that a camera is no longer connected to a computer, 
#  whether it was disconnected by unplugging a cord, opening
#   the compact flash compartment, 
#   turning the camera off, auto shut-off, or by other means. 
	Shutdown				= 0x00000301

#  Notifies of whether or not there are objects waiting to
#   be transferred to a host computer. 
#  This is useful when ensuring all shot images have been transferred 
#  when the application is closed. 
#  Notification of this event is not issued for type 1 protocol 
#  standard cameras. 
	JobStatusChanged		= 0x00000302

#  Notifies that the camera will shut down after a specific period. 
#  Generated only if auto shut-off is set. 
#  Exactly when notification is issued (that is, the number of
#   seconds until shutdown) varies depending on the camera model. 
#  To continue operation without having the camera shut down,
#  use EdsSendCommand to extend the auto shut-off timer.
#  The time in seconds until the camera shuts down is returned
#   as the initial value. 
	WillSoonShutDown		= 0x00000303

#  As the counterpart event to kEdsStateEvent_WillSoonShutDown,
#  this event notifies of updates to the number of seconds until
#   a camera shuts down. 
#  After the update, the period until shutdown is model-dependent. 
	ShutDownTimerUpdate		= 0x00000304

#  Notifies that a requested release has failed, due to focus
#   failure or similar factors. 
	CaptureError			= 0x00000305

#  Notifies of internal SDK errors. 
#  If this error event is received, the issuing device will probably
#   not be able to continue working properly,
#   so cancel the remote connection. 
	InternalError			= 0x00000306
	AfResult				= 0x00000309	
	BulbExposureTime		= 0x00000310	
	PowerZoomInfoChanged	= 0x00000311	

class PropertyEvent:
#  Property Event

#  Notifies all property events. 
	All						= 0x00000100

#  Notifies that a camera property value has been changed. 
#  The changed property can be retrieved from event data. 
#  The changed value can be retrieved by means of EdsGetPropertyData. 
#  If the property type is 0x0000FFFF, the changed property cannot be identified. 
#  Thus, retrieve all required properties repeatedly. 
	PropertyChanged			= 0x00000101

#  Notifies of changes in the list of camera properties with configurable values. 
#  The list of configurable values for property IDs indicated in event data 
#   can be retrieved by means of EdsGetPropertyDesc. 
#  For type 1 protocol standard cameras, the property ID is identified as "Unknown"
#   during notification. 
#   Thus, you must retrieve a list of configurable values for all properties and
#   retrieve the property values repeatedly. 
#  (For details on properties for which you can retrieve a list of configurable
#   properties, 
#   see the description of EdsGetPropertyDesc). 
	PropertyDescChanged		= 0x00000102

class ObjectEvent:
#  Object Event

#  Notifies all object events. 
	All                         = 0x00000200

#  Notifies that the volume object (memory card) state (VolumeInfo)
#   has been changed. 
#  Changed objects are indicated by event data. 
#  The changed value can be retrieved by means of EdsGetVolumeInfo. 
#  Notification of this event is not issued for type 1 protocol standard cameras. 
	VolumeInfoChanged           = 0x00000201

#  Notifies if the designated volume on a camera has been formatted.
#  If notification of this event is received, get sub-items of the designated
#   volume again as needed. 
#  Changed volume objects can be retrieved from event data. 
#  Objects cannot be identified on cameras earlier than the D30
#   if files are added or deleted. 
#  Thus, these events are subject to notification. 
	VolumeUpdateItems           = 0x00000202

#  Notifies if many images are deleted in a designated folder on a camera.
#  If notification of this event is received, get sub-items of the designated
#   folder again as needed. 
#  Changed folders (specifically, directory item objects) can be retrieved
#   from event data. 
	FolderUpdateItems           = 0x00000203

#  Notifies of the creation of objects such as new folders or files
#   on a camera compact flash card or the like. 
#  This event is generated if the camera has been set to store captured
#   images simultaneously on the camera and a computer,
#   for example, but not if the camera is set to store images
#   on the computer alone. 
#  Newly created objects are indicated by event data. 
#  Because objects are not indicated for type 1 protocol standard cameras,
#   (that is, objects are indicated as NULL),
#  you must again retrieve child objects under the camera object to 
#  identify the new objects. 
	DirItemCreated              = 0x00000204

#  Notifies of the deletion of objects such as folders or files on a camera
#   compact flash card or the like. 
#  Deleted objects are indicated in event data. 
#  Because objects are not indicated for type 1 protocol standard cameras, 
#  you must again retrieve child objects under the camera object to
#   identify deleted objects. 
	DirItemRemoved              = 0x00000205

#  Notifies that information of DirItem objects has been changed. 
#  Changed objects are indicated by event data. 
#  The changed value can be retrieved by means of EdsGetDirectoryItemInfo. 
#  Notification of this event is not issued for type 1 protocol standard cameras. 
	DirItemInfoChanged          = 0x00000206

#  Notifies that header information has been updated, as for rotation information
#   of image files on the camera. 
#  If this event is received, get the file header information again, as needed. 
#  This function is for type 2 protocol standard cameras only. 
	DirItemContentChanged       = 0x00000207

#  Notifies that there are objects on a camera to be transferred to a computer. 
#  This event is generated after remote release from a computer or local release
#   from a camera. 
#  If this event is received, objects indicated in the event data must be downloaded.
#   Furthermore, if the application does not require the objects, instead
#   of downloading them,
#    execute EdsDownloadCancel and release resources held by the camera. 
#  The order of downloading from type 1 protocol standard cameras must be the order
#   in which the events are received. 
	DirItemRequestTransfer      = 0x00000208

#  Notifies if the camera's direct transfer button is pressed. 
#  If this event is received, objects indicated in the event data must be downloaded. 
#  Furthermore, if the application does not require the objects, instead of
#   downloading them, 
#   execute EdsDownloadCancel and release resources held by the camera. 
#  Notification of this event is not issued for type 1 protocol standard cameras. 
	DirItemRequestTransferDT    = 0x00000209

#  Notifies of requests from a camera to cancel object transfer 
#   if the button to cancel direct transfer is pressed on the camera. 
#  If the parameter is 0, it means that cancellation of transfer is requested for
#   objects still not downloaded,
#   with these objects indicated by kEdsObjectEvent_DirItemRequestTransferDT. 
#  Notification of this event is not issued for type 1 protocol standard cameras. 
	DirItemCancelTransferDT     = 0x0000020a

	VolumeAdded                 = 0x0000020c
	VolumeRemoved               = 0x0000020d
