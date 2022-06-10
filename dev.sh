#!/bin/sh

die() {
	case $# in
		0 )
			exit 1
			;;
		1 )
			printf '%s\n' "$1" >&2
			exit 1
			;;
		* )
			printf '%s\n' "$1" >&2
			exit "$2"
			;;
	esac
}

clean() {
	[ -f .coverage ] && { echo 'Removing: ./.coverage'; rm .coverage; }
	[ -d .pytest_temp ] && { echo 'Removing: ./.pytest_temp'; rm -rf .pytest_temp; }
	find . -path ./virtualenv -prune \
		-o -type d -name __pycache__ -print \
		-o -type d -name .pytest_cache -print \
	| while read line; do
		echo "Removing: $line"
		rm -r -- "$line"
	done
}

: ${CAPTURE:=true}

cd "$(dirname "$0")"

if ! [ $# -eq 1 ]; then
	die 'Dev script only takes 1 argument'
fi

subcommand=$1

[ -d virtualenv ] && . virtualenv/bin/activate

case "$subcommand" in
	virtualenv )
		virtualenv virtualenv
		. virtualenv/bin/activate
		pip install pytest
		pip install coverage
		;;
	purge )
		clean
		[ -d virtualenv ] && rm -r virtualenv
		;;
	clean )
		clean
		;;
	test )
		[ -d virtualenv ] || die 'no virtualenv'
		if [ "$CAPTURE" = false ]; then
			coverage run -m pytest -s tests
		else
			coverage run -m pytest tests
		fi
		;;
	coverage )
		[ -d virtualenv ] || die 'no virtualenv'
		coverage report
		;;
esac
