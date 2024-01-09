from mutant.directory.manager import MutantDirectory

def main(args):
	if args.action == 'create':
		args.mutant_dir.create_mutation(args.directory)
