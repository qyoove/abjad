# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class ScorePackageWrangler(Wrangler):
    r'''Score package wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            ScorePackageWrangler()

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = scoremanager.wranglers.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            ScorePackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(ScorePackageWrangler, self)
        superclass.__init__(session=session)
        path = self._configuration.example_score_packages_directory_path
        self._abjad_storehouse_path = path
        path = self._configuration.user_score_packages_directory_path
        self._user_storehouse_path = path
        self._manager_class = managers.ScorePackageManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        breadcrumb = 'scores'
        view_name = self._read_view_name()
        if view_name:
            breadcrumb = '{} ({} view)'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _current_storehouse_path(self):
        if self._session.is_in_score:
            path = self._configuration.example_score_packages_directory_path
            directory_entries = sorted(os.listdir(path))
            manager = self._session.current_score_package_manager
            score_name = manager._package_name
            if score_name in directory_entries:
                return path
            else:
                return self._configuration.user_score_packages_directory_path
        else:
            return self._configuration.user_score_packages_directory_path

#    @property
#    def _user_input_to_action(self):
#        superclass = super(ScorePackageWrangler, self)
#        result = superclass._user_input_to_action
#        result = result.copy()
#        result.update({
#            'new': self.make_score_package,
#            'rm': self.remove_score_packages,
#            })
#        return result

    @property
    def _user_input_to_action(self):
        result = {
            'cp': self.copy_score,
            'cro': self.view_cache,
            'cw': self.write_cache,
            'd': self.manage_distribution_artifact_library,
            'fix': self.fix_score_packages,
            'g': self.manage_segment_library,
            'k': self.manage_maker_library,
            'm': self.manage_material_library,
            'mdme': self.edit_metadata_modules,
            'mdmls': self.list_metadata_modules,
            'mdmrw': self.rewrite_metadata_modules,
            'new': self.make_score_package,
            'pyd': self.doctest,
            'pyt': self.pytest,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'ren': self.rename_score_package,
            'rm': self.remove_score_packages,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rup': self.update_from_repository,
            'ssl': self.display_all_scores,
            'ssv': self.display_active_scores,
            'ssmb': self.display_mothballed_scores,
            'ssx': self.display_example_scores,
            'ssu': self.display_user_scores,
            'u': self.manage_build_file_library,
            'va': self.apply_view,
            'vls': self.list_views,
            'vnew': self.make_view,
            'vren': self.rename_view,
            'vrm': self.remove_views,
            'vmrm': self.remove_views_module,
            'vmro': self.view_views_module,
            'V': self.clear_view,
            'y': self.manage_stylesheet_library,
            }
        return result

    ### PRIVATE METHODS ###

    def _find_git_manager(self, must_have_file=False):
        superclass = super(ScorePackageWrangler, self)
        manager = superclass._find_git_manager(
            inside_score=False,
            must_have_file=must_have_file,
            )
        return manager

    def _find_svn_manager(self, must_have_file=False):
        superclass = super(ScorePackageWrangler, self)
        manager = superclass._find_svn_manager(
            inside_score=False,
            must_have_file=must_have_file,
            )
        return manager

    def _get_sibling_score_directory_path(self, next_=True):
        paths = self._list_visible_asset_paths()
        if self._session.last_asset_path is None:
            if next_:
                return paths[0]
            else:
                return paths[-1]
        score_path = self._session.last_asset_path
        index = paths.index(score_path)
        if next_:
            sibling_index = (index + 1) % len(paths)
        else:
            sibling_index = (index - 1) % len(paths)
        sibling_path = paths[sibling_index]
        return sibling_path
        
    def _get_sibling_score_path(self):
        if self._session.is_navigating_to_next_score:
            self._session._is_navigating_to_next_score = False
            self._session._is_backtracking_to_score_manager = False
            return self._get_sibling_score_directory_path(next_=True)
        if self._session.is_navigating_to_previous_score:
            self._session._is_navigating_to_previous_score = False
            self._session._is_backtracking_to_score_manager = False
            return self._get_sibling_score_directory_path(next_=False)

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            score_package_paths = self._list_visible_asset_paths()
            if result in score_package_paths:
                self.manage_score(result)

    def _is_valid_directory_entry(self, expr):
        superclass = super(ScorePackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _list_all_directories_with_metadata_modules(self):
        storehouses = (
            self._configuration.abjad_material_packages_directory_path,
            self._configuration.example_score_packages_directory_path,
            self._configuration.user_library_directory_path,
            self._configuration.user_score_packages_directory_path,
            )
        directories = []
        for storehouse in storehouses:
            result = self._list_directories_with_metadata_modules(storehouse)
            directories.extend(result)
        return directories

    def _list_visible_asset_paths(
        self,
        abjad_library=True,
        user_library=True,
        example_score_packages=True,
        user_score_packages=True,
        ):
        visible_paths = []
        paths = self._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        for path in paths:
            manager = self._initialize_manager(path)
            if manager._is_visible() != False:
                visible_paths.append(path)
        return visible_paths

    def _make_asset_menu_entries(
        self,
        apply_view=True,
        include_annotation=True,
        include_extensions=False,
        include_asset_name=False,
        include_year=True,
        human_readable=True,
        packages_instead_of_paths=False,
        sort_by_annotation=True,
        ):
        superclass = super(ScorePackageWrangler, self)
        menu_entries = superclass._make_asset_menu_entries(
            apply_view=apply_view,
            include_annotation=include_annotation,
            include_extensions=include_extensions,
            include_asset_name=include_asset_name,
            include_year=include_year,
            human_readable=human_readable,
            packages_instead_of_paths=packages_instead_of_paths,
            sort_by_annotation=sort_by_annotation,
            )
        return menu_entries

    def _get_scores_to_display_string(self):
        return '{} scores'.format(self._session.scores_to_display)

    def _make_all_directories_menu_section(self, menu):
        commands = []
        string = 'all dirs - metadata module - edit'
        commands.append((string, 'mdme'))
        string = 'all dirs - metadata module - list'
        commands.append((string, 'mdmls'))
        string = 'all dirs - metadata module - rewrite'
        commands.append((string, 'mdmrw'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='all dirs',
            )

    def _make_all_score_packages_menu_section(self, menu):
        commands = []
        commands.append(('all score packages - fix', 'fix'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='all score packages',
            )

    def _make_cache_menu_section(self, menu):
        commands = []
        commands.append(('cache - read only', 'cro'))
        commands.append(('cache - write', 'cw'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='cache',
            )

    def _make_main_menu(self):
        menu = self._make_score_selection_menu()
        self._make_all_directories_menu_section(menu)
        self._make_all_score_packages_menu_section(menu)
        self._make_scores_menu_section(menu)
        self._make_scores_show_menu_section(menu)
        self._make_cache_menu_section(menu)
        self._make_views_menu_section(menu)
        self._make_views_module_menu_section(menu)
        return menu

    def _make_score_selection_menu(self):
        if self._session.rewrite_cache:
            self._io_manager.write_cache(prompt=False)
            self._session._rewrite_cache = False
        menu_entries = self._io_manager._read_cache()
        if (not menu_entries or
            (self._session._scores_to_display == 'example' and
            not menu_entries[0][0] == 'Blue Example Score (2013)')):
            self._io_manager.write_cache(prompt=False)
            menu_entries = self._io_manager._read_cache()
        menu = self._io_manager.make_menu(
            name='main',
            breadcrumb_callback=self._get_scores_to_display_string,
            )
        menu.make_asset_section(
            menu_entries=menu_entries,
            )
        return menu

    def _make_scores_menu_section(self, menu):
        commands = []
        commands.append(('scores - copy', 'cp'))
        commands.append(('scores - new', 'new'))
        commands.append(('scores - remove', 'rm'))
        commands.append(('scores - rename', 'ren'))
        menu.make_command_section(
            commands=commands,
            name='scores',
            )

    def _make_scores_show_menu_section(self, menu):
        commands = []
        commands.append(('scores - show all', 'ssl'))
        commands.append(('scores - show active', 'ssv'))
        commands.append(('scores - show examples', 'ssx'))
        commands.append(('scores - show mothballed', 'ssmb'))
        commands.append(('scores - show user', 'ssu'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='scores - show',
            )

    ### PUBLIC METHODS ###

    def make_score_package(self):
        r'''Makes score package.

        Returns none.
        '''
        path = self._get_available_path()
        if self._should_backtrack():
            return
        if not path:
            return
        self._make_asset(path)
        self._io_manager.write_cache(prompt=False)

    def manage_score(self, path):
        r'''Manages score.

        Returns none.
        '''
        manager = self._initialize_manager(path)
        package_name = os.path.basename(path)
        manager.fix(prompt=True)
        manager._run()

    def remove_score_packages(self):
        r'''Removes one or more score packages.
        
        Returns none.
        '''
        self._remove_assets(
            item_identifier='score package',
            )

    def rename_score_package(self):
        r'''Renames score package.

        Returns none.
        '''
        self._rename_asset(
            item_identifier='score package',
            )

    ### MIGRATED OVER ###

#    def add_to_repository(self, prompt=True):
#        r'''Adds assets to repository.
#
#        Returns none.
#        '''
#        self.add_to_repository(prompt=prompt)

#    def apply_view(self):
#        r'''Applies view.
#
#        Returns none.
#        '''
#        self.apply_view()

#    def clear_view(self):
#        r'''Clears view.
#
#        Returns none.
#        '''
#        self.clear_view()

#    def commit_to_repository(self, prompt=True):
#        r'''Commits assets to repository.
#
#        Returns none.
#        '''
#        self.commit_to_repository()

    def copy_score(self):
        r'''Copies score package.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def display_active_scores(self):
        r'''Displays active scores.

        Returns none.
        '''
        self._session.display_active_scores()

    def display_all_scores(self):
        r'''Displays all scores.

        Returns none.
        '''
        self._session.display_all_scores()

    def display_example_scores(self):
        r'''Displays example scores.

        Returns none.
        '''
        self._session.display_example_scores()

    def display_mothballed_scores(self):
        r'''Displays mothballed scores.

        Returns none.
        '''
        self._session.display_mothballed_scores()

    def display_user_scores(self):
        r'''Displays user scores.

        Returns none.
        '''
        self._session.display_user_scores()

#    def doctest(self):
#        r'''Runs doctest on visible score packages.
#
#        Returns none.
#        '''
#        self.doctest()

    def edit_metadata_modules(self):
        r'''Edits all metadata modules everywhere.

        Ignores view.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_modules()
        paths = [os.path.join(_, '__metadata__.py') for _ in directories]
        self._io_manager.view(paths)

    def fix_score_packages(self, prompt=True):
        r'''Fixes score packages.

        Returns none.
        '''
        from scoremanager import managers
        #wrangler = self._score_package_wrangler
        #paths = wrangler._list_visible_asset_paths()
        paths = self._list_visible_asset_paths()
        for path in paths:
            manager = managers.ScorePackageManager(
                path=path,
                session=self._session,
                )
            needed_to_be_fixed = manager.fix(prompt=prompt)
            if not needed_to_be_fixed:
                title = manager._get_title()
                message = '{} OK.'
                message = message.format(title)
                self._io_manager.display(message)
        message = '{} score packages checked.'
        message = message.format(len(paths))
        self._io_manager.display(['', message, ''])
        self._io_manager.proceed(prompt=prompt)

    def list_metadata_modules(self, prompt=True):
        r'''Lists all metadata modules everywhere.

        Ignores view.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_modules()
        paths = [os.path.join(_, '__metadata__.py') for _ in directories]
        lines = paths[:]
        lines.append('')
        if prompt:
            self._io_manager.display(lines)
        message = '{} metadata modules found.'
        message = message.format(len(paths))
        self._io_manager.proceed(message, prompt=prompt)

#    def list_views(self):
#        r'''Lists views.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.list_views()

#    def make_score_package(self):
#        r'''Makes new score.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.make_score_package()

#    def make_view(self):
#        r'''Makes view.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.make_view()

    def manage_build_file_library(self):
        r'''Manages build file library.

        Returns none.
        '''
        self._session._score_manager._build_file_wrangler._run()

    def manage_distribution_artifact_library(self):
        r'''Manages distribution file library.

        Returns none.
        '''
        self._session._score_manager._distribution_file_wrangler._run()

    def manage_maker_library(self):
        r'''Manages maker library.

        Returns none.
        '''
        self._session._score_manager._maker_module_wrangler._run()

    def manage_material_library(self):
        r'''Manages material library.

        Returns none.
        '''
        self._session._score_manager._material_package_wrangler._run()

#    def manage_score(self, path):
#        r'''Manages score.
#
#        Returns none.
#        '''
#        manager = self._score_package_wrangler._initialize_manager(path)
#        package_name = os.path.basename(path)
#        manager.fix(prompt=True)
#        manager._run()

    def manage_segment_library(self):
        r'''Manages segment library.

        Returns none.
        '''
        self._session._score_manager._segment_package_wrangler._run()

    def manage_stylesheet_library(self):
        r'''Manages stylesheet library.

        Returns none.
        '''
        self._session._score_manager._stylesheet_wrangler._run()

#    def pytest(self):
#        r'''Runs py.test.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.pytest()

#    def remove_score_packages(self):
#        r'''Removes score package.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.remove_score_packages()

#    def remove_views(self):
#        r'''Removes view(s) from views module.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.remove_views()

#    def remove_views_module(self):
#        r'''Removes views module.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.remove_views_module()

#    def rename_score_package(self):
#        r'''Renames score package.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.rename_score_package()

#    def rename_view(self):
#        r'''Renames view.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.rename_view()

#    def repository_status(self, prompt=True):
#        r'''Displays status of repository assets.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.repository_status(prompt=prompt)

#    def revert_to_repository(self, prompt=True):
#        r'''Reverts modified assets and unadds added assets.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.revert_to_repository(prompt=prompt)

    def rewrite_metadata_modules(self, prompt=True):
        r'''Rewrites all metadata modules everywhere.

        Ignores view.

        Returns none.
        '''
        from scoremanager import managers
        directories = self._list_all_directories_with_metadata_modules()
        for directory in directories:
            manager = managers.PackageManager(
                path=directory,
                session=self._session,
                )
            manager.rewrite_metadata_module(prompt=False)
        message = '{} metadata modules found.'
        message = message.format(len(directories))
        self._io_manager.proceed(message, prompt=prompt)

#    def update_from_repository(self, prompt=True):
#        r'''Updates repository assets.
#
#        Returns none.
#        '''
#        self._score_package_wrangler.update_from_repository()

    def view_cache(self):
        r'''Views cache.

        Returns none.
        '''
        file_path = self._configuration.cache_file_path
        self._io_manager.open_file(file_path)
        self._session._hide_next_redraw = True

#    def view_views_module(self):
#        r'''View views module.
#
#        Return none.
#        '''
#        print('FOO')
#        self._score_package_wrangler.view_views_module()

    def write_cache(self, prompt=True):
        r'''Writes cache.

        Returns none.
        '''
        self._io_manager.write_cache(prompt=prompt)