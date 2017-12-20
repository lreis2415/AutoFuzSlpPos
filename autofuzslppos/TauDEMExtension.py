#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Extensions based on TauDEM framework.

    @author   : Liangjun Zhu

    @changelog: 17-08-01  lj - initial implementation based on pygeoc.\n
"""

import os

from pygeoc.TauDEM import TauDEM
from pygeoc.utils import StringClass


class TauDEMExtension(TauDEM):
    """Extension functions based on TauDEM."""

    def __init__(self):
        """Initialize TauDEM."""
        TauDEM.__init__(self)

    @staticmethod
    def d8distuptoridge(np, workingdir, p, fel, src, dist, distm,
                        mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run D8 distance to stream"""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('d8distuptoridge', exedir),
                          {'-fel': fel, '-p': p, '-src': src},
                          {'-m': TauDEM.convertdistmethod(distm)},
                          {'-du': dist}, {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def dinfdistuptoridge(np, workingdir, ang, fel, slp, propthresh, dist, statsm, distm,
                          edgecontamination, rdg=None,
                          mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run Dinf distance to ridge."""
        os.chdir(workingdir)
        in_params = {'-thresh': str(propthresh),
                     '-m': '%s %s' % (TauDEM.convertstatsmethod(statsm),
                                      TauDEM.convertdistmethod(distm))}
        if StringClass.string_match(edgecontamination, 'false') or edgecontamination is False:
            in_params['-nc'] = None
        return TauDEM.run(TauDEM.fullpath('dinfdistuptoridge', exedir),
                          {'-ang': ang, '-fel': fel, '-slp': slp, '-rdg': rdg},
                          in_params,
                          {'-du': dist}, {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def extractridge(np, workingdir, angfile, elevfile, rdgsrc,
                     mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Extract ridge source."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('ridgeextraction', exedir),
                          {'-dir': angfile, '-fel': elevfile},
                          None,
                          {'-src': rdgsrc},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def rpiskidmore(np, workingdir, vlysrc, rdgsrc, rpi, vlytag=1, rdgtag=1, dist2vly=None,
                    dist2rdg=None, mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Calculate RPI according to Skidmore (1990)."""
        os.chdir(workingdir)
        in_params = dict()
        if vlytag > 0:
            in_params['-vlytag'] = vlytag
        if rdgtag > 0:
            in_params['-rdgtag'] = rdgtag
        return TauDEM.run(TauDEM.fullpath('rpiskidmore', exedir),
                          {'-vly': vlysrc, '-rdg': rdgsrc},
                          in_params,
                          {'-rpi': rpi, '-dist2vly': dist2vly, '-dist2rdg': dist2rdg},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def curvature(np, workingdir, fel, profc, horizc=None, planc=None, unspherc=None, avec=None,
                  maxc=None, minc=None, mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Calculate various curvature."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('curvature', exedir),
                          {'-fel': fel}, None,
                          {'-prof': profc, '-plan': planc, '-horiz': horizc,
                           '-unspher': unspherc, '-ave': avec, '-max': maxc, '-min': minc},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def simplecalculator(np, workingdir, inputa, inputb, output, operator,
                         mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Run simple calculator.

           operator = 0: add
                      1: minus
                      2: multiply
                      3: divide
                      4: a/(a+b)
                      5: mask
        """
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('simplecalculator', exedir),
                          {'-in': [inputa, inputb]},
                          {'-op': operator},
                          {'-out': output},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def selecttyplocslppos(np, workingdir, inputconf, outputconf, extlog=None,
                           mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Select typical locations."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('selecttyplocslppos', exedir),
                          {'-in': inputconf}, None,
                          {'-out': outputconf, '-extlog': extlog},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def fuzzyslpposinference(np, workingdir, config, mpiexedir=None,
                             exedir=None, log_file=None, hostfile=None):
        """Run fuzzy inference."""
        os.chdir(workingdir)
        return TauDEM.run(TauDEM.fullpath('fuzzyslpposinference', exedir),
                          {'-in': config}, None, None,
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})

    @staticmethod
    def hardenslppos(np, workingdir, simifiles, tags, hard, maxsimi,
                     sechard=None, secsimi=None, spsim=None, spsi=None,
                     mpiexedir=None, exedir=None, log_file=None, hostfile=None):
        """Select typical locations."""
        os.chdir(workingdir)
        if len(simifiles) != len(tags):
            raise RuntimeError("hardenslppos: simifiles and tags must have the same size!")
        tag_path = ''
        for i, tag in enumerate(tags):
            tag_path += ' %d %s ' % (tag, simifiles[i])
        in_params = dict()
        if spsim is not None and spsi is not None:
            in_params['-m'] = '%d %s' % (spsim, spsi)
        return TauDEM.run(TauDEM.fullpath('hardenslppos', exedir),
                          {'-inf': '%d %s' % (len(simifiles), tag_path)},
                          in_params,
                          {'-maxS': [hard, maxsimi], '-secS': [sechard, secsimi]},
                          {'mpipath': mpiexedir, 'hostfile': hostfile, 'n': np},
                          {'logfile': TauDEM.fullpath(log_file, workingdir)})
