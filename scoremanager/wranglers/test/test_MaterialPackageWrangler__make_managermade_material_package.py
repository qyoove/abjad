# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager



def test_MaterialPackageWrangler__make_managermade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testsargasso'
    assert not wrangler._configuration.package_exists(string)
    filesystem_path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )

    try:
        wrangler._make_managermade_material_package(
            filesystem_path, 
            'SargassoMeasureMaterialManager',
            )
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            filesystem_path=filesystem_path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)


def test_MaterialPackageWrangler__make_managermade_material_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.example_numbers'
    assert wrangler._configuration.package_exists(string)
    statement = "wrangler._make_managermade_material_package("
    statement += "'scoremanager.materials.example_sargasso_measures"
    statement += "'SargassoMeasureMaterialManager')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler__make_managermade_material_package_03():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testsargasso'
    assert not wrangler._configuration.package_exists(string)
    filesystem_path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_managermade_material_package(
            filesystem_path, 
            'SargassoMeasureMaterialManager', 
            metadata=metadata,
            )
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            filesystem_path=filesystem_path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)
