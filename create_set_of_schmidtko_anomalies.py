
import os
import settings
import create_schmidtko_anomaly

for model in settings.models:
    for scenario in settings.scenarios:

        try:
            out_file = create_schmidtko_anomaly.copy_cmip_file(settings, model, scenario)
            create_schmidtko_anomaly.anomalize_to_schmidtko(out_file, settings.schmidtko_file)
            create_schmidtko_anomaly.add_coordinate_variables(out_file,settings.schmidtko_file)
            create_schmidtko_anomaly.rename_ocean_variable(out_file)
        except IOError as error:
            print(error)
            continue

