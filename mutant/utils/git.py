import subprocess

class Repo:
	def __init__(self, path):
		self.path = path

	def _run(self, *args, **kwargs):
		return subprocess.run(*args, **kwargs, cwd=self.path)

	def init(self, commit_message="First commit"):
		commands = (
			('git', 'init'),
			('git', 'add', '-A'),
			('git', 'commit', '-m', commit_message),
		)
		for command in commands:
			self._run(command)
		return self

	def remote_add(self, name, url):
		self._run(( 'git', 'remote', 'add', '--', name, url ))
		return self

	def add_all(self):
		self._run(('git', 'add', '-A'))
		return self

	def commit(self, message='commit'):
		self._run(( 'git', 'commit', '-a', '-m', message))
		return self

	@classmethod
	def clone(cls, url, dst):
		subprocess.run(
			('git', 'clone', '--', url, str(dst))
		)
		return cls(dst)
