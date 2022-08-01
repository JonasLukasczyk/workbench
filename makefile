SCRATCH_DIR=testing/scratch
NEW_SCRATCH_DIR=testing/scratcher
TEST_DIR=$(SCRATCH_DIR)/example

clean:
	rm -rf build
	rm -rf cinemasci.egg-info
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
	@echo "Creating test area ..."
	@cp -rf cinemasci $(TEST_DIR)
	@./cinema --database $(TEST_DIR)/cinema.cdb
	@cp -rf testing/gold/artifact/sphere.cdb $(TEST_DIR)
	@cp examples/demoCDB.ipynb $(TEST_DIR)
	@cp examples/hello.ipynb $(TEST_DIR)
	@cp examples/image.ipynb $(TEST_DIR)
	@cp examples/image_convert.ipynb $(TEST_DIR)
	@cp examples/image_canny.ipynb $(TEST_DIR)
	@cp examples/imageArtifactSource.ipynb $(TEST_DIR)
	@cp examples/parameterWidgets.ipynb $(TEST_DIR)
	@echo "Running jupyter notebook ..."
	@cd $(TEST_DIR); jupyter notebook image_canny.ipynb
