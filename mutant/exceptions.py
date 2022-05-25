class ConfigFileError(Exception):
	"Exception for situations where a configuration file is invalid."
	pass

class LimitedProcessError(Exception):
	"Exception that is specific to mutant.utils.process.LimitedProcess"
	pass

class LimitExceededError(LimitedProcessError):
	"Output limit set in LimitedProcess is exceeded"
	pass

class LPBrokenPipeError(LimitedProcessError, BrokenPipeError):
	"Broken pipe error in LimitedProcess"
	pass

class M4Error(Exception):
	"Exception that is related to m4"
	pass
