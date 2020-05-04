#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Cyrille Favreau <cyrille.favreau@gmail.com>
#
# This file is part of pyPhaneron
# <https://github.com/favreau/pyPhaneron>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

import seaborn as sns
import math


class MeshDescriptor(object):

    def __init__(self, assembly_name, name, contents, assembly_radius,
                 recenter=True, occurrences=1, random_seed=0,
                 orientation=[1, 0, 0, 0]):
        self.assembly_name = assembly_name
        self.name = name
        self.contents = contents
        self.assembly_radius = assembly_radius
        self.recenter = recenter
        self.occurrences = occurrences
        self.random_seed = random_seed
        self.orientation = orientation


class ProteinDescriptor(object):

    def __init__(self, assembly_name, name, contents, assembly_radius,
                 atom_radius_multiplier=1, load_bonds=False, add_sticks=False,
                 chain_ids=list(), recenter=True, occurrences=1, random_seed=0,
                 location_cutoff_angle=0.998, orientation=[1, 0, 0, 0]):
        self.assembly_name = assembly_name
        self.name = name
        self.contents = contents
        self.assembly_radius = assembly_radius
        self.atom_radius_multiplier = atom_radius_multiplier
        self.load_bonds = load_bonds
        self.add_sticks = add_sticks
        self.chain_ids = chain_ids
        self.recenter = recenter
        self.occurrences = occurrences
        self.random_seed = random_seed
        self.location_cutoff_angle = location_cutoff_angle
        self.orientation = orientation


class GlycansDescriptor(object):

    def __init__(self, assembly_name, name, contents, protein_name, atom_radius_multiplier=1, add_sticks=False,
                 recenter=True, site_indices=list()):
        self.assembly_name = assembly_name
        self.name = name
        self.contents = contents
        self.protein_name = protein_name
        self.atom_radius_multiplier = atom_radius_multiplier
        self.add_sticks = add_sticks
        self.recenter = recenter
        self.site_indices = site_indices


class RNASequenceDescriptor(object):

    def __init__(self, assembly_name, name, contents, shape, assembly_radius, radius, t_range=None,
                 shape_params=None):
        self.assembly_name = assembly_name
        self.name = name
        self.contents = contents
        self.shape = shape
        self.assembly_radius = assembly_radius
        self.radius = radius
        self.t_range = t_range
        self.shape_params = shape_params


class BioExplorer(object):
    MODEL_CONTENT_TYPE_PDB = 0
    MODEL_CONTENT_TYPE_OBJ = 1

    COLOR_SCHEME_NONE = 0
    COLOR_SCHEME_ATOMS = 1
    COLOR_SCHEME_CHAINS = 2
    COLOR_SCHEME_RESIDUES = 3
    COLOR_SCHEME_AMINO_ACID_SEQUENCE = 4
    COLOR_SCHEME_GLYCOSYLATION_SITE = 5

    RNA_SHAPE_TREFOIL_KNOT = 0
    RNA_SHAPE_TORUS = 1
    RNA_SHAPE_STAR = 2
    RNA_SHAPE_SPRING = 3
    RNA_SHAPE_HEART = 4
    RNA_SHAPE_THING = 5
    RNA_SHAPE_MOEBIUS = 6

    IMAGE_QUALITY_LOW = 0
    IMAGE_QUALITY_HIGH = 1

    """ VirusExplorer """

    def __init__(self, client):
        """
        Create a new Steps instance
        """
        self._client = client

    def __str__(self):
        """Return a pretty-print of the class"""
        return "Virus Explorer for Brayns"

    def reset(self):
        ids = list()
        for model in self._client.scene.models:
            ids.append(model['id'])
        self._client.remove_model(array=ids)

    def remove_assembly(self, name):
        params = dict()
        params['name'] = name
        params['position'] = [0, 0, 0]
        params['halfStructure'] = False
        params['clippingPlanes'] = list()
        result = self._client.rockets_client.request(method='remove-assembly', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])

    def add_assembly(self, name, position=[0, 0, 0], half_structure=False, clipping_planes=list()):
        clipping_planes_values = list()
        for plane in clipping_planes:
            for i in range(4):
                clipping_planes_values.append(plane[i])

        params = dict()
        params['name'] = name
        params['position'] = position
        params['halfStructure'] = half_structure
        params['clippingPlanes'] = clipping_planes_values
        result = self._client.rockets_client.request(method='add-assembly', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def set_protein_color_scheme(self, protein_descriptor, color_scheme, palette_name, palette_size=256):
        palette = sns.color_palette(palette_name, palette_size)
        p = list()
        for color in palette:
            for i in range(3):
                p.append(color[i])

        params = dict()
        params['assemblyName'] = protein_descriptor.assembly_name
        params['name'] = protein_descriptor.name
        params['colorScheme'] = color_scheme
        params['palette'] = p
        result = self._client.rockets_client.request(method='set-protein-color-scheme', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def set_protein_amino_acid_sequence_as_string(self, protein_descriptor, amino_acid_sequence):
        params = dict()
        params['assemblyName'] = protein_descriptor.assembly_name
        params['name'] = protein_descriptor.name
        params['sequence'] = amino_acid_sequence
        result = self._client.rockets_client.request(method='set-protein-amino-acid-sequence-as-string', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def set_protein_amino_acid_sequence_as_range(self, protein_descriptor, amino_acid_range):
        params = dict()
        params['assemblyName'] = protein_descriptor.assembly_name
        params['name'] = protein_descriptor.name
        params['range'] = amino_acid_range
        result = self._client.rockets_client.request(method='set-protein-amino-acid-sequence-as-range', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def show_amino_acid_on_protein(self, protein, sequence_id=0, palette_name='Set1', palette_size=2):
        from ipywidgets import IntRangeSlider, Label
        from IPython.display import display

        sequences = self.get_protein_amino_acid_sequences(protein)
        if sequence_id >= len(sequences):
            raise RuntimeError('Invalid sequence Id')

        irs = IntRangeSlider(value=[0, 100], min=0, max=len(sequences[sequence_id]))
        lbl = Label(value="AA sequence")

        def update_slider(v):
            self.set_protein_amino_acid_sequence_as_range(protein, v['new'])
            self.set_protein_color_scheme(protein, self.COLOR_SCHEME_AMINO_ACID_SEQUENCE, palette_name, palette_size)
            lbl.value = sequences[sequence_id][v['new'][0]:v['new'][1]]

        irs.observe(update_slider, 'value')
        display(irs)
        display(lbl)

    def get_protein_amino_acid_sequences(self, protein_descriptor):
        params = dict()
        params['assemblyName'] = protein_descriptor.assembly_name
        params['name'] = protein_descriptor.name
        result = self._client.rockets_client.request(method='get-protein-amino-acid-sequences', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        return result['contents'].split()

    def add_rna_sequence(self, rna_sequence_descriptor):

        t_range = [0.0, 2.0 * math.pi]
        if rna_sequence_descriptor.t_range is None:
            ''' Defaults '''
            if rna_sequence_descriptor.shape == self.RNA_SHAPE_TORUS:
                t_range = [0.0, 2.0 * math.pi]
            elif rna_sequence_descriptor.shape == self.RNA_SHAPE_TREFOIL_KNOT:
                t_range = [0.0, 4.0 * math.pi]
        else:
            t_range = rna_sequence_descriptor.t_range

        shape_params = [1.0, 1.0, 1.0]
        if rna_sequence_descriptor.shape_params is None:
            ''' Defaults '''
            if rna_sequence_descriptor.shape == self.RNA_SHAPE_TORUS:
                shape_params = [0.5, 10.0, 0.0]
            elif rna_sequence_descriptor.shape == self.RNA_SHAPE_TREFOIL_KNOT:
                shape_params = [2.5, 2.0, 2.2]

        else:
            shape_params = rna_sequence_descriptor.shape_params

        params = dict()
        params['assemblyName'] = rna_sequence_descriptor.assembly_name
        params['name'] = rna_sequence_descriptor.name
        params['contents'] = rna_sequence_descriptor.contents
        params['shape'] = rna_sequence_descriptor.shape
        params['assemblyRadius'] = rna_sequence_descriptor.assembly_radius
        params['radius'] = rna_sequence_descriptor.radius
        params['range'] = t_range
        params['params'] = shape_params
        result = self._client.rockets_client.request(method='add-rna-sequence', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def add_protein(self, protein_descriptor):
        params = dict()
        params['assemblyName'] = protein_descriptor.assembly_name
        params['name'] = protein_descriptor.name
        params['contents'] = protein_descriptor.contents
        params['assemblyRadius'] = protein_descriptor.assembly_radius
        params['atomRadiusMultiplier'] = protein_descriptor.atom_radius_multiplier
        params['loadBonds'] = protein_descriptor.load_bonds
        params['addSticks'] = protein_descriptor.add_sticks
        params['chainIds'] = protein_descriptor.chain_ids
        params['recenter'] = protein_descriptor.recenter
        params['occurrences'] = protein_descriptor.occurrences
        params['randomSeed'] = protein_descriptor.random_seed
        params['locationCutoffAngle'] = protein_descriptor.location_cutoff_angle
        params['orientation'] = protein_descriptor.orientation
        result = self._client.rockets_client.request(method='add-protein', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def add_mesh(self, mesh_descriptor):
        params = dict()
        params['assemblyName'] = mesh_descriptor.assembly_name
        params['name'] = mesh_descriptor.name
        params['contents'] = mesh_descriptor.contents
        params['assemblyRadius'] = mesh_descriptor.assembly_radius
        params['recenter'] = mesh_descriptor.recenter
        params['occurrences'] = mesh_descriptor.occurrences
        params['randomSeed'] = mesh_descriptor.random_seed
        params['orientation'] = mesh_descriptor.orientation
        result = self._client.rockets_client.request(method='add-mesh', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def add_glycans(self, glycans_descriptor):
        params = dict()
        params['assemblyName'] = glycans_descriptor.assembly_name
        params['name'] = glycans_descriptor.name
        params['contents'] = glycans_descriptor.contents
        params['proteinName'] = glycans_descriptor.protein_name
        params['atomRadiusMultiplier'] = glycans_descriptor.atom_radius_multiplier
        params['addSticks'] = glycans_descriptor.add_sticks
        params['recenter'] = glycans_descriptor.recenter
        params['siteIndices'] = glycans_descriptor.site_indices
        result = self._client.rockets_client.request(method='add-glycans', params=params)
        if not result['status']:
            raise RuntimeError(result['contents'])
        self._client.set_renderer(accumulation=True)

    def set_image_quality(self, image_quality=IMAGE_QUALITY_LOW):
        if image_quality == self.IMAGE_QUALITY_HIGH:
            self._client.set_renderer(
                background_color=[0, 0, 0],
                current='circuit_explorer_advanced',
                samples_per_pixel=1, subsampling=4)
            params = self._client.CircuitExplorerAdvancedRendererParams()
            params.gi_samples = 1
            params.gi_weight = 0.01
            params.gi_distance = 1e6
            params.shadows = 0.75
            params.soft_shadows = 1
            params.fog_start = 10
            params.fog_thickness = 1e6
            params.exposure = 1
            params.volume_alpha_correction = 1
            self._client.set_renderer_params(params)
        else:
            self._client.set_renderer(
                background_color=[0, 0, 0],
                current='basic',
                samples_per_pixel=1, subsampling=4)
