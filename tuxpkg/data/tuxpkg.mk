version = $(shell sed -e '/^__version__/ !d; s/"\s*$$//; s/.*"//' $(PROJECT)/__init__.py)

rpm: dist/$(PROJECT)-$(version)-0$(PROJECT).noarch.rpm

RPMBUILD = rpmbuild
dist/$(PROJECT)-$(version)-0$(PROJECT).noarch.rpm: dist/$(PROJECT)-$(version).tar.gz dist/$(PROJECT).spec
	cd dist && \
	$(RPMBUILD) -ta --define "dist $(PROJECT)" --define "_rpmdir $$(pwd)" $(PROJECT)-$(version).tar.gz
	mv $(patsubst dist/%, dist/noarch/%, $@) $@
	rmdir dist/noarch

rpmsrc: dist dist/$(PROJECT).spec

dist/$(PROJECT).spec: $(PROJECT).spec
	cp $(PROJECT).spec dist/

dist: dist/$(PROJECT)-$(version).tar.gz

dist/$(PROJECT)-$(version).tar.gz:
	flit build

deb: debsrc dist/$(PROJECT)_$(version)-1_all.deb

dist/$(PROJECT)_$(version)-1_all.deb: dist/$(PROJECT)_$(version)-1.dsc
	cd dist/$(PROJECT)-$(version) && dpkg-buildpackage -b -us -uc

debsrc: dist dist/$(PROJECT)_$(version)-1.dsc dist/$(PROJECT)_$(version).orig.tar.gz

dist/$(PROJECT)_$(version).orig.tar.gz: dist/$(PROJECT)-$(version).tar.gz
	ln -f $< $@

dist/$(PROJECT)_$(version)-1.dsc: debian dist/$(PROJECT)_$(version).orig.tar.gz $(wildcard debian/*)
	cd dist && tar xaf $(PROJECT)_$(version).orig.tar.gz
	cp -r debian/ dist/$(PROJECT)-$(version)
	cd dist/$(PROJECT)-$(version)/ && dpkg-buildpackage -S -d -us -uc
