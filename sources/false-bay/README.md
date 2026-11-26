# False Bay ERA5 snapshots

Retrieved 2026-11-26. These files preserve the Open-Meteo API responses. The underlying ERA5 reanalysis is from the Copernicus Climate Change Service. Wind is 10 m wind speed in m/s at the returned cell (-34.25, 18.50). Wave height is total significant wave height in metres at the returned offshore cell (-34.50, 18.50). The offshore value is a regional sea-state proxy.

- [Wind request](https://archive-api.open-meteo.com/v1/archive?latitude=-34.25&longitude=18.50&start_date=2022-06-06&end_date=2022-06-28&hourly=wind_speed_10m&timezone=Africa%2FJohannesburg&models=era5&cell_selection=nearest&wind_speed_unit=ms)
- [Wave request](https://marine-api.open-meteo.com/v1/marine?latitude=-34.20&longitude=18.62&start_date=2022-06-06&end_date=2022-06-28&hourly=wave_height&timezone=Africa%2FJohannesburg&models=era5_ocean&cell_selection=sea)
- [ERA5 single levels](https://doi.org/10.24381/cds.adbb2d47)
- [Playback study](https://doi.org/10.12688/openreseurope.24618.1)

SHA-256 wind.json: 98024e1efae9edf22f782d0dce322527815a51154c9837e9582e909b125ca299

SHA-256 wave.json: afd7b356d893b61f0a7bae70ff3f0d7e4cf5624b958af2c7508cef9b49d890ca

Both APIs returned Africa/Johannesburg timestamps at UTC+02:00. The analysis selects the six hourly timestamps 08:00 through 13:00 on each of the 12 Data02 dates. Runtime reads only these archived files.
