# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr


def _hydrogen_flow(STH, irradiance):
    """
    Computes the hydrogen flow (kWh/s) of a PEC-Module. Assumes the module area
    to be 1 m2.

    STH: float
        Solar-to-hydrogen efficiency

    irradiance: np.array
        Irradiance (W/m2)

    Return hydrogen flow. (kW/ (m**2))
    """

    dG_r0 = 237.13e3  # (J/mol) Gibbs free energy change for water splitting at standard conditions (25°C, 1 atm)
    M_H2 = 0.002  # Molar weight of hydrogen molecule (kg/mol)
    LHV_H2 = 33.33 * 3600  # Lower heating value of hydrogen (kJ/kg)

    flow_mol_time = (STH * irradiance) / dG_r0  # (mol/(s m²))

    flow_kg_time = flow_mol_time * M_H2 * LHV_H2  # (kJ/(s m²))

    # FIXME: Fix units/names (currently not fitting together kg and kW)!
    return flow_kg_time  # (kW/ (m**2))


def _flow_baggie(irradiance, pc):
    # Temperature independent STH efficiency
    STH = pc["STH"]

    # Reference flow:
    flow_ref = _hydrogen_flow(STH, pc["r_irradiance"])

    # Hydrogen flow

    # Calculate the hydrogen flow rate for the module temperature and irradiance
    flow = _hydrogen_flow(STH, irradiance)

    da = flow / flow_ref

    # If irradiance computation fails, replace NAN with 0.0
    da = da.fillna(0.0).clip(min=0)

    # All energy values are related to the lower heating value of hydrogen.
    da.attrs["units"] = "kWh/kWp"
    da = da.rename("specific generation")

    return da


# Function like SolarPanelModel() in solar_panel_model.py
def PhotocatalysisPanelModel(ds, irradiance, pc):
    """
    Hydrogen flow calculation.

    Args:
        ds (xarray.DataSet): data set containing temperature data etc.
        irradiance (xarray.DataArray): data array containing irradiance values
        pc (dict): dictionary with module / baggie configuration and information
    Returns:
        xarray.DataArray: Data array containing the hydrogen flow
    """
    model = pc.get("model", "baggie")
    if model == "baggie":
        return _flow_baggie(irradiance, pc)
    else:
        AssertionError("Unknown panel model: {}".format(model))


def create_sample_data(
    constant_irradiance=None,
    temp_range=None,
    irradiance_range=None,
    constant_temperature=None,
):
    np.random.seed(0)

    # Define the dimensions
    x = np.linspace(0, 1999, 2000)
    y = np.linspace(0, 1, 2)
    time = pd.date_range("2023-01-01", periods=1)

    # Define the coordinates
    lon, lat = np.meshgrid(x, y)

    # Create some sample data
    shape = (1, 2, 2000)  # (time, y, x)

    if constant_irradiance is not None and temp_range is not None:
        # Constant irradiance with temperature range
        irradiation_data = np.full(shape, constant_irradiance)
        temperature_data = np.linspace(
            temp_range[0], temp_range[1], num=np.prod(shape)
        ).reshape(shape)
    elif irradiance_range is not None and constant_temperature is not None:
        # Irradiance range with constant temperature
        irradiation_data = np.linspace(
            irradiance_range[0], irradiance_range[1], num=np.prod(shape)
        ).reshape(shape)
        temperature_data = np.full(shape, constant_temperature)
    else:
        raise ValueError(
            "You must provide either (constant_irradiance and temp_range) or (irradiance_range and constant_temperature)."
        )

    # Create the DataArray for irradiation
    irradiance = xr.DataArray(
        irradiation_data,
        name="random_irr_values",
        coords={
            "time": time,
            "x": x,
            "y": y,
            "lon": (["y", "x"], lon),
            "lat": (["y", "x"], lat),
        },
        dims=["time", "y", "x"],
        attrs={"units": "W m**-2"},
    )

    # Create the DataArray for temperature
    temperature = xr.DataArray(
        temperature_data,
        name="random_temp_values",
        coords={
            "time": time,
            "x": x,
            "y": y,
            "lon": (["y", "x"], lon),
            "lat": (["y", "x"], lat),
        },
        dims=["time", "y", "x"],
        attrs={
            "module": "era5",
            "prepared_features": ["temperature", "influx"],
        },
    )

    ds = xr.Dataset({"irradiation": irradiance, "temperature": temperature})

    return irradiance, ds


if __name__ == "__main__":
    pc_type = "baggie"
    if pc_type == "baggie":
        pc = {
            "model": "baggie",
            "name": "baggie",
            "source": None,
            "r_irradiance": 1000,
            "characteristic_length": 1,
            "emissivity": 0.84,
            "irradiation_type": "total",
            "STH": 0.11,
        }

    # Constant irradiance with temperature range
    irradiance_1, ds_1 = create_sample_data(
        constant_irradiance=1000.0, temp_range=(250.0, 450.0)
    )
    res_1 = PhotocatalysisPanelModel(ds_1, irradiance_1, pc)

    # Irradiance range with constant temperature
    irradiance_2, ds_2 = create_sample_data(
        irradiance_range=(600.0, 800.0), constant_temperature=290.15
    )
    res_2 = PhotocatalysisPanelModel(ds_2, irradiance_2, pc)

    fig, ax = plt.subplots()
    ax.plot(ds_1["temperature"][0][0], res_1[0][0], label=irradiance_1[0][0][0].values)
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Capacity Factor")
    ax.grid()
    ax.legend()
    plt.show()
    fig, ax = plt.subplots()
    ax.plot(irradiance_2[0][0], res_2[0][0], label=ds_2["temperature"][0][0][0].values)
    ax.set_xlabel("Irradiance")
    ax.set_ylabel("Capacity Factor")
    ax.grid()
    ax.legend()
    plt.show()
