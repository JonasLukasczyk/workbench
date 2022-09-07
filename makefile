SCRATCH_DIR=testing/scratch
NEW_SCRATCH_DIR=testing/scratcher
TEST_DIR=$(SCRATCH_DIR)/example

null:
	@:

clean:
	rm -rf build
	rm -rf pycinema.egg-info
	rm -rf dist
	rm -rf $(SCRATCH_DIR) 

example:
	@rm -rf $(TEST_DIR)
	@if [ ! -d "$(SCRATCH_DIR)" ]; then\
		echo "Creating scratch dir";\
		mkdir $(SCRATCH_DIR);\
	fi
	@if [ ! -d "$(TEST_DIR)" ]; then\
		echo "Creating test dir";\
		mkdir $(TEST_DIR);\
	fi
	@echo "Creating test area $(TEST_DIR)"
	@cp -rf pycinema $(TEST_DIR)
	@./cinema --database $(TEST_DIR)/cinema.cdb
	@mkdir $(TEST_DIR)/testing
	@mkdir $(TEST_DIR)/testing/gold
	@mkdir $(TEST_DIR)/testing/gold/artifact
	@mkdir $(TEST_DIR)/testing/gold/artifact/MLModels
	@cp -rf testing/gold/artifact/sphere.cdb $(TEST_DIR)/testing/gold/artifact
	@cp -rf testing/DragonImages.cdb $(TEST_DIR)/testing
	@cp examples/*.ipynb $(TEST_DIR)
	@cp examples/*.py $(TEST_DIR)
	@cp testing/gold/artifact/MLModels/*.pth $(TEST_DIR)/testing/gold/artifact/MLModels

module:
	rm -rf build
	rm -rf *.egg-info
	rm -rf dist
	python3 setup.py sdist

module-upload:
	twine upload dist/*
