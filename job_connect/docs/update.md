Once you've made changes to your Django project (like adding new models, modifying views, updating docstrings, etc.), you'll need to regenerate or rebuild your Sphinx documentation to reflect those changes. Here's a breakdown of the steps involved:

# TL;DR
1. **Regenerate API docs** with `sphinx-apidoc -f` if your code has changed.
2. **Update any manual `.rst` or `.md` files.**
3. **Rebuild the documentation** with `make html`.
4. **Review the output.**

By following these steps, you can keep your Sphinx documentation up-to-date with the evolving state of your Django project. Remember to run `sphinx-apidoc` with the `-f` (force) flag to ensure that the existing API documentation files are overwritten with the latest information.

## Full Version
1. **Regenerate API Documentation (if applicable):** If your changes include modifications to your Python code (models, views, forms, etc.) and you're using `sphinx-apidoc` to automatically generate API documentation, you'll need to run the `sphinx-apidoc` command again to pick up those changes.
    
    Navigate to the root of your Django project in the terminal and run:
    
    ```Bash
    sphinx-apidoc -o docs/source/ your_project_name -f -e "venv*" -e "*migrations*"
    ```
    
    - Replace `your_project_name` with the name of your main project directory (the one containing `settings.py`).
    - The `-o docs/source/` option specifies the output directory for the generated `.rst` files.
    - The `-f` option tells `sphinx-apidoc` to overwrite any existing files. This is important to ensure your documentation reflects the latest state of your code.
    - The `-e` options are to exclude your virtual environment and migrations directories, as you likely don't want to document those. Adjust these as needed for your project.
    
    If you have specific apps you want to regenerate documentation for, you can target those instead of the whole project:
    
    ```Bash
    sphinx-apidoc -o docs/source/ your_app_name -f
    ```
    
2. **Update Manual Documentation:** If you've written any parts of your documentation manually in `.rst` or `.md` files, you'll need to go through those files and update them to reflect the changes you've made in your project. This might involve:
    
    - Adding documentation for new features.
    - Modifying existing documentation to reflect changes in functionality.
    - Updating code examples.
3. **Rebuild the Sphinx Documentation:** After regenerating the API documentation (if needed) and updating your manual documentation, you need to rebuild the HTML (or other formats) using Sphinx.
    
    Navigate to your `docs` directory in the terminal and run:
    
    ```Bash
    make html
    ```
    
    This command will process all your `.rst` and `.md` files (including the newly generated ones) and create the updated documentation in the `docs/_build/html` directory.
    
4. **Review the Updated Documentation:** It's crucial to review the generated documentation in your web browser to ensure that:
    
    - The changes you made in your Django project are accurately reflected.
    - There are no new warnings or errors in the Sphinx build output.
    - The navigation and links are still working correctly.

