""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np

from philoseismos.models.layer import Layer
from philoseismos.segy.segy import SegY


class HorizontallyLayeredMedium:
    """ This object represents a horizontally layered medium.

     Horizontally layered medium is a collection of horizontal layers stacked on top of a half-space.

     """

    def __init__(self, *, vp=None, vs=1000, rho=None, q=None):
        """ Create a new HorizontallyLayeredMedium.

        Only accepts keyword arguments. Vp and Rho will be computed automatically if no provided.

        Args:
            vp: P-wave velocity in the half-space in m/s.
            vs: S-wave velocity in a half space in m/s.
            rho: Density of the half-space in kg/m^3.

        """

        self.vs = vs
        self.vp = vp if vp else vs * np.sqrt(3)  # assume that Lame parameters are equal and vp = vs * sqrt(3)
        self.rho = rho if rho else 310 * self.vp ** 0.25  # use the Gardner's relation to compute rho
        self.q = q

        self._layers = []

    def add_layer(self, *, vp=None, vs=300, rho=None, h=10, q=None):
        """ Add a layer on top of the medium. """

        self._layers.append(Layer(vp=vp, vs=vs, rho=rho, h=h, q=q))

    def pop_layer(self, index=-1):
        """ Remove and return layer at index (default last). """

        return self._layers.pop(index)

    def get_profiles(self, *, half_space_depth=10):
        """ Return profiles of all the parameters to plot.

        Returns:
            z, vp, vs, rho, q: Matplotlib-ready parameter profiles.

        """

        z = [0]
        vp = []
        vs = []
        rho = []
        q = []

        for layer in reversed(self._layers):
            z += [z[-1] + layer.h] * 2
            vp += [layer.vp] * 2
            vs += [layer.vs] * 2
            rho += [layer.rho] * 2
            q += [layer.q] * 2

        z += [z[-1] + half_space_depth]
        vp += [self.vp] * 2
        vs += [self.vs] * 2
        rho += [self.rho] * 2
        q += [self.q] * 2

        return z, vp, vs, rho, q

    def export_for_tesseral(self, x0, x1, base_filename, *,
                            dz=0.01, half_space_depth=100):
        """ Export model to SEG-Y format for use in Tesseral.

        Args:
            x0 : Start of the x axis.
            x1 : End of the x axis.
            base_filename : Base file name for resulting SEG-Y files. The parameter name and
                file extension will be appended automatically.
            dz: Discretization step for z-axis in m. Default to 1 cm.
            half_space_depth: How deep should the half-space be in the model.

        Notes:
            Creates three SEG-Y files: one with values of Vp, one with values of Vs, and one
            with values of rho.

        """

        hs = [layer.h for layer in self._layers]
        z1 = sum(hs) + half_space_depth
        zz = np.repeat(np.arange(0, z1 + dz, dz)[np.newaxis, :], 2, axis=0)

        vps = np.empty_like(zz, dtype=np.float32)
        vss = np.empty_like(zz, dtype=np.float32)
        rhos = np.empty_like(zz, dtype=np.float32)
        qs = np.empty_like(zz, dtype=np.float32)

        if self._layers:
            vps[:, 0] = self._layers[-1].vp
            vss[:, 0] = self._layers[-1].vs
            rhos[:, 0] = self._layers[-1].rho
            qs[:, 0] = self._layers[-1].q
        else:
            vps[:, 0] = self.vp
            vss[:, 0] = self.vs
            rhos[:, 0] = self.rho
            qs[:, 0] = self.q

        depth = 0
        for layer in reversed(self._layers):
            vps[(zz > depth) & (zz <= depth + layer.h)] = layer.vp
            vss[(zz > depth) & (zz <= depth + layer.h)] = layer.vs
            rhos[(zz > depth) & (zz <= depth + layer.h)] = layer.rho
            qs[(zz > depth) & (zz <= depth + layer.h)] = layer.q

            depth += layer.h

        vps[zz > depth] = self.vp
        vss[zz > depth] = self.vs
        rhos[zz > depth] = self.rho
        qs[zz > depth] = self.q

        vps_sgy = SegY.from_matrix(vps, sample_interval=int(dz * 1000))
        vss_sgy = SegY.from_matrix(vss, sample_interval=int(dz * 1000))
        rhos_sgy = SegY.from_matrix(rhos, sample_interval=int(dz * 1000))
        qs_sgy = SegY.from_matrix(qs, sample_interval=int(dz * 1000))

        for sgy in (vps_sgy, vss_sgy, rhos_sgy, qs_sgy):
            sgy.g.REC_X = [x0, x1]

        vps_sgy.save(f'{base_filename}_vp.sgy')
        vss_sgy.save(f'{base_filename}_vs.sgy')
        rhos_sgy.save(f'{base_filename}_rho.sgy')
        qs_sgy.save(f'{base_filename}_q.sgy')

    def __repr__(self):
        vp = f'vp={self.vp}' if self.vp == int(self.vp) else f'vp≈{round(self.vp)}'
        vs = f'vs={self.vs}' if self.vs == int(self.vs) else f'vs≈{round(self.vs)}'
        rho = f'rho={self.rho}' if self.rho == int(self.rho) else f'rho≈{round(self.rho)}'
        return f'HorizontallyLayeredMedium({vp}, {vs}, {rho})'

    def __str__(self):
        out = ''

        for i, l in enumerate(reversed(self._layers)):
            vp = f'vp={l.vp}' if l.vp == int(l.vp) else f'vp≈{round(l.vp)}'
            vs = f'vs={l.vs}' if l.vs == int(l.vs) else f'vs≈{round(l.vs)}'
            rho = f'rho={l.rho}' if l.rho == int(l.rho) else f'rho≈{round(l.rho)}'
            h = f'h={l.h}' if l.h == round(l.h, 2) else f'h≈{round(l.h, 2)}'
            out += f'Layer #{i}: {vp} {vs} {rho} {h}\n'

        vp = f'vp={self.vp}' if self.vp == int(self.vp) else f'vp≈{round(self.vp)}'
        vs = f'vs={self.vs}' if self.vs == int(self.vs) else f'vs≈{round(self.vs)}'
        rho = f'rho={self.rho}' if self.rho == int(self.rho) else f'rho≈{round(self.rho)}'
        out += f'Half-space: {vp} {vs} {rho}'
        return out
