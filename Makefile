README.md: README.rst
	pandoc --from=rst --to=markdown README.rst > README.md
	sed -i 's/{.sourceCode}//' README.md
