#!/usr/bin/env python

import shutil
import tempfile
import os.path
import numpy as np
from xml.dom import minidom
from amptools.table import read_excel, dataframe_to_xml
import pandas as pd

def test_write_xml():
    homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?
    datadir = os.path.join(homedir,'..','data')
    complete_file = os.path.join(datadir,'complete_pgm.xlsx')
    mmimin_file = os.path.join(datadir,'minimum_mmi.xlsx')
    tempdir = None
    try:
        tempdir = tempfile.mkdtemp()
        df, reference = read_excel(complete_file)
        _ = dataframe_to_xml(df,'foo',tempdir,reference=reference)
        
        df_mmimin,reference = read_excel(mmimin_file)
        _ = dataframe_to_xml(df_mmimin,'bar',tempdir,reference=reference)
        
    except Exception:
        raise AssertionError('Could not write XML file.')
    finally:
        if tempdir is not None:
            shutil.rmtree(tempdir)

def test_read_tables():
    homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?
    datadir = os.path.join(homedir,'..','data')

    ##########################################
    # these files should all read successfully
    ##########################################
    
    complete_file = os.path.join(datadir,'complete_pgm.xlsx')
    df_complete,_ = read_excel(complete_file)
    np.testing.assert_almost_equal(df_complete['h1']['pga'].sum(),569.17)
        
    pgamin_file = os.path.join(datadir,'minimum_pga.xlsx')
    df_pgamin,_ = read_excel(pgamin_file)
    np.testing.assert_almost_equal(df_pgamin['unk']['pga'].sum(),569.17)
    

    mmimin_file = os.path.join(datadir,'minimum_mmi.xlsx')
    df_mmimin, _ = read_excel(mmimin_file)
    np.testing.assert_almost_equal(df_mmimin['intensity'].sum(),45.199872273516036)

    missing_data_file = os.path.join(datadir,'missing_rows.xlsx')
    df,reference = read_excel(missing_data_file)
    assert np.isnan(df['h1']['psa03']['CHPA'])

    sm2xml_example = os.path.join(datadir,'sm2xml_output.xlsx')
    df,reference = read_excel(sm2xml_example)
    np.testing.assert_almost_equal(df['hhz']['pga'].sum(),150.82342541678645)
    
    ##########################################
    # these files should all fail
    ##########################################
    try:
        missing_file = os.path.join(datadir,'missing_columns.xlsx')
        read_excel(missing_file)
        assert 1==2
    except KeyError:
        assert 1==1

    try:
        wrong_file = os.path.join(datadir,'wrong_channels.xlsx')
        read_excel(wrong_file)
        assert 1==2
    except KeyError:
        assert 1==1

    try:
        nodata_file = os.path.join(datadir,'no_data.xlsx')
        read_excel(nodata_file)
        assert 1==2
    except KeyError:
        assert 1==1

    try:
        emptyrow_file = os.path.join(datadir,'empty_row.xlsx')
        read_excel(emptyrow_file)
        assert 1==2
    except IndexError:
        assert 1==1

    try:
        noref_file = os.path.join(datadir,'no_reference.xlsx')
        read_excel(noref_file)
        assert 1==2
    except KeyError:
        assert 1==1


def test_dataframe_to_xml():
    homedir = os.path.dirname(os.path.abspath(__file__)) #where is this script?
    datadir = os.path.join(homedir,'..','data')
    amps_output = os.path.join(datadir,'amps.csv')
    df = pd.read_csv(amps_output)
    outdir = os.path.expanduser('~')
    try:
        xmlfile = dataframe_to_xml(df,'foo',outdir)
        # HNN,psa10,0.0107
        root = minidom.parse(xmlfile)
        comps = root.getElementsByTagName('comp')
        for comp in comps:
            if comp.getAttribute('name') == 'HNN':
                psa10 = comp.getElementsByTagName('psa10')[0]
                value = float(psa10.getAttribute('value'))
                assert value == 0.0107
    except Exception:
        assert 1==2
    finally:
        if os.path.isfile(xmlfile):
            os.remove(xmlfile)
if __name__ == '__main__':
    test_write_xml()
    test_read_tables()
    test_dataframe_to_xml()
    
