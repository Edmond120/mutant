import subprocess

class Repo:
	def __init__(self, path):
		self.path = path

	def _run(self, *args, **kwargs):
		process = subprocess.run(*args, **kwargs, cwd=self.path)
		if process.returncode != 0:
			raise RuntimeError(f'Command failed: {process}')

	def init(self, message="First commit"):
		self._run(('git', 'init'))
		self.add_all()
		self.commit(message)
		return self

	def remote_add(self, name, url):
		self._run(( 'git', 'remote', 'add', '--', name, url ))
		return self

	def add_all(self):
		self._run(('git', 'add', '-A'))
		return self

	def commit(self, message='Commit'):
		self._run(( 'git', 'commit', '-a', '-m', message))
		return self

	@classmethod
	def clone(cls, url, dst):
		subprocess.run(
			('git', 'clone', '--', url, str(dst))
		)
		return cls(dst)
