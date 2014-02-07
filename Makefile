SHELL=/bin/bash

# https://code.google.com/p/protobuf/
PROTOC := $(shell which protoc)
PROTO_DIR=protobuf-2.5.0
PROTO_TAR=$(PROTO_DIR).tar.gz
PROTO_SRC=https://protobuf.googlecode.com/files/$PROTO_TAR
PROTO_PY=modernart_pb2.py

# main rules

run: $(PROTO_PY)
	python main.py

clean:
	rm -rf build/* *.pyc $(PROTO_PY)

# conditional rules for building Python proto file, varies to avoid
# dependancy on protoc when it will be unused

ifdef PROTOC
$(PROTO_PY): modernart.proto
	protoc --python_out=. modernart.proto
else
$(PROTO_PY): protoc  modernart.proto
	protoc --python_out=. modernart.proto
endif

# automatic proto compiler and proto Python library installation

ifndef PROTOC
$(PROTO_TAR):
	curl https://protobuf.googlecode.com/files/protobuf-2.5.0.tar.gz \
		-o build/$(PROTO_TAR)
protoc: build/$(PROTO_TAR)
	@echo trying to auto-build and install protoc, will prompt for sudo
	sudo echo got root
	cd build && tar xfz $(PROTO_TAR)
	cd build/$(PROTO_DIR) && \
		./configure && \
		make && \
		sudo make install
	cd build/$(PROTO_DIR)/python && \
		python setup.py build && \
		python setup.py test && \
		sudo python setup.py install
endif
