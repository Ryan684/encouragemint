from django.forms import model_to_dict

from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.models.profile import Profile

SAMPLE_GARDEN = {"garden_name": "Foo", "direction": "north", "location": "Truro, UK"}
SAMPLE_GARDEN_SUNLIGHT = "low"
SAMPLE_GARDEN_GEOCODE_LOCATION = {
    "address": SAMPLE_GARDEN.get("location"),
    "latitude": 50.263195,
    "longitude": -5.051041
}
SAMPLE_PLANT = {
    "scientific_name": "Eriophyllum lanatum",
    "common_name": "common woolly sunflower",
    "duration": "Annual, Perennial",
    "bloom_period": "Spring",
    "growth_period": "Summer",
    "growth_rate": "Slow",
    "shade_tolerance": "High",
    "moisture_use": "High",
    "family_common_name": "Aster family",
    "trefle_id": 134845
}


def create_test_garden():
    profile = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
    garden = {"garden_name": "Foo", "direction": "north", "location": "Truro, UK",
              "profile": profile, "latitude": 50.263195, "longitude": -5.051041}

    test_garden = Garden.objects.create(**garden)
    return model_to_dict(test_garden)


TREFLE_NAME_LOOKUP_RESPONSE = [
    {
        "slug": "eriophyllum-lanatum",
        "scientific_name": "Eriophyllum lanatum",
        "link": "http://trefle.io/api/plants/134845",
        "id": 134845,
        "complete_data": False,
        "common_name": "common woolly sunflower"
    }
]

TREFLE_ID_LOOKUP_RESPONSE = {
    "varieties": [
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134859,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:09.156306"
                }
            ],
            "slug": "eriophyllum-lanatum-var-leucophyllum",
            "scientific_name": "Eriophyllum lanatum var. leucophyllum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134859",
            "is_main_species": False,
            "id": 134859,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134849,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.181210"
                }
            ],
            "slug": "eriophyllum-lanatum-var-croceum",
            "scientific_name": "Eriophyllum lanatum var. croceum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134849",
            "is_main_species": False,
            "id": 134849,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134856,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.860143"
                }
            ],
            "slug": "eriophyllum-lanatum-var-lanatum",
            "scientific_name": "Eriophyllum lanatum var. lanatum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134856",
            "is_main_species": False,
            "id": 134856,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134851,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.383133"
                }
            ],
            "slug": "eriophyllum-lanatum-var-grandiflorum",
            "scientific_name": "Eriophyllum lanatum var. grandiflorum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134851",
            "is_main_species": False,
            "id": 134851,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134850,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.285304"
                },
                {
                    "species_id": 134850,
                    "source_url": "http://www.tropicos.org",
                    "name": "Tropicos",
                    "last_update": "2019-01-12T07:21:02.186035"
                }
            ],
            "slug": "eriophyllum-lanatum-var-cuneatum",
            "scientific_name": "Eriophyllum lanatum var. cuneatum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134850",
            "is_main_species": False,
            "id": 134850,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134847,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:07.983091"
                },
                {
                    "species_id": 134847,
                    "source_url": "http://www.tropicos.org",
                    "name": "Tropicos",
                    "last_update": "2019-01-12T07:21:03.153879"
                }
            ],
            "slug": "eriophyllum-lanatum-var-aphanactis",
            "scientific_name": "Eriophyllum lanatum var. aphanactis",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134847",
            "is_main_species": False,
            "id": 134847,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134846,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:07.885241"
                }
            ],
            "slug": "eriophyllum-lanatum-var-achillaeoides",
            "scientific_name": "Eriophyllum lanatum var. achillaeoides",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134846",
            "is_main_species": False,
            "id": 134846,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134857,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.957324"
                }
            ],
            "slug": "eriophyllum-lanatum-var-typicum",
            "scientific_name": "Eriophyllum lanatum var. typicum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134857",
            "is_main_species": False,
            "id": 134857,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134848,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.081448"
                }
            ],
            "slug": "eriophyllum-lanatum-var-arachnoideum",
            "scientific_name": "Eriophyllum lanatum var. arachnoideum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134848",
            "is_main_species": False,
            "id": 134848,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134855,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.766175"
                },
                {
                    "species_id": 134855,
                    "source_url": "http://www.tropicos.org",
                    "name": "Tropicos",
                    "last_update": "2019-01-12T07:21:02.191545"
                }
            ],
            "slug": "eriophyllum-lanatum-var-monoense",
            "scientific_name": "Eriophyllum lanatum var. monoense",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134855",
            "is_main_species": False,
            "id": 134855,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134858,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:09.056212"
                }
            ],
            "slug": "eriophyllum-lanatum-var-lanceolatum",
            "scientific_name": "Eriophyllum lanatum var. lanceolatum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134858",
            "is_main_species": False,
            "id": 134858,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134860,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:09.254150"
                }
            ],
            "slug": "eriophyllum-lanatum-var-obovatum",
            "scientific_name": "Eriophyllum lanatum var. obovatum",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134860",
            "is_main_species": False,
            "id": 134860,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134852,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.479160"
                }
            ],
            "slug": "eriophyllum-lanatum-var-hallii",
            "scientific_name": "Eriophyllum lanatum var. hallii",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134852",
            "is_main_species": False,
            "id": 134852,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Unknown",
            "sources": [
                {
                    "species_id": 134853,
                    "source_url": "https://plants.usda.gov",
                    "name": "USDA",
                    "last_update": "2019-01-11T10:11:08.577011"
                }
            ],
            "slug": "eriophyllum-lanatum-var-integrifolium",
            "scientific_name": "Eriophyllum lanatum var. integrifolium",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/134853",
            "is_main_species": False,
            "id": 134853,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": None,
            "author": None
        },
        {
            "year": None,
            "type": "var",
            "synonym": False,
            "status": "Accepted",
            "sources": [
                {
                    "species_id": 260375,
                    "source_url": "http://www.tropicos.org",
                    "name": "Tropicos",
                    "last_update": "2019-01-12T07:21:02.806434"
                }
            ],
            "slug": "eriophyllum-lanatum-var-achillioides",
            "scientific_name": "Eriophyllum lanatum var. achillioides",
            "main_species_id": 134845,
            "link": "http://trefle.io/api/plants/260375",
            "is_main_species": False,
            "id": 260375,
            "family_common_name": "Aster family",
            "complete_data": False,
            "common_name": "common woolly sunflower",
            "bibliography": "A Manual of the Flowering Plants of California"
                            " . . . 1118. 1925. (Man. Fl. Pl. Calif.) ",
            "author": "Jeps."
        }
    ],
    "sub_species": [],
    "scientific_name": "Eriophyllum lanatum",
    "order": None,
    "native_status": "L48(N)CAN(N)",
    "main_species": {
        "year": None,
        "type": "species",
        "synonym": False,
        "status": "Unknown",
        "specifications": {
            "toxicity": None,
            "shape_and_orientation": None,
            "regrowth_rate": None,
            "nitrogen_fixation": None,
            "max_height_at_base_age": {
                "ft": None,
                "cm": None
            },
            "mature_height": {
                "ft": None,
                "cm": None
            },
            "low_growing_grass": None,
            "lifespan": None,
            "leaf_retention": None,
            "known_allelopath": None,
            "growth_rate": "Slow",
            "growth_period": "Summer",
            "growth_habit": None,
            "growth_form": None,
            "fire_resistance": None,
            "fall_conspicuous": None,
            "coppice_potential": None,
            "c_n_ratio": None,
            "bloat": None
        },
        "sources": [
            {
                "species_id": 134845,
                "source_url": "https://plants.usda.gov",
                "name": "USDA",
                "last_update": "2019-01-11T10:11:07.785008"
            }
        ],
        "soils_adaptation": {
            "medium": None,
            "fine": None,
            "coarse": None
        },
        "slug": "eriophyllum-lanatum",
        "seed": {
            "vegetative_spread_rate": None,
            "small_grain": None,
            "seeds_per_pound": None,
            "seedling_vigor": None,
            "seed_spread_rate": None,
            "commercial_availability": None,
            "bloom_period": "Spring"
        },
        "scientific_name": "Eriophyllum lanatum",
        "propagation": {
            "tubers": None,
            "sprigs": None,
            "sod": None,
            "seed": None,
            "cuttings": None,
            "corms": None,
            "container": None,
            "bulbs": None,
            "bare_root": None
        },
        "products": {
            "veneer": None,
            "pulpwood": None,
            "protein_potential": None,
            "post": None,
            "palatable_human": None,
            "palatable_graze_animal": None,
            "palatable_browse_animal": None,
            "nursery_stock": None,
            "naval_store": None,
            "lumber": None,
            "fuelwood": None,
            "fodder": None,
            "christmas_tree": None,
            "berry_nut_seed": None
        },
        "native_status": "L48(N)CAN(N)",
        "main_species_id": None,
        "is_main_species": True,
        "images": [
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons"
                       "/b/b9/Eriophyllum_lanatum_3575.JPG"
            }
        ],
        "id": 134845,
        "growth": {
            "temperature_minimum": {
                "deg_f": None,
                "deg_c": None
            },
            "shade_tolerance": "High",
            "salinity_tolerance": None,
            "root_depth_minimum": {
                "inches": None,
                "cm": None
            },
            "resprout_ability": None,
            "precipitation_minimum": {
                "inches": None,
                "cm": None
            },
            "precipitation_maximum": {
                "inches": None,
                "cm": None
            },
            "planting_density_minimum": {
                "sqm": None,
                "acre": None
            },
            "planting_density_maximum": {
                "sqm": None,
                "acre": None
            },
            "ph_minimum": None,
            "ph_maximum": None,
            "moisture_use": "High",
            "hedge_tolerance": None,
            "frost_free_days_minimum": None,
            "fire_tolerance": None,
            "fertility_requirement": None,
            "drought_tolerance": None,
            "cold_stratification_required": None,
            "caco_3_tolerance": None,
            "anaerobic_tolerance": None
        },
        "fruit_or_seed": {
            "seed_persistence": None,
            "seed_period_end": None,
            "seed_period_begin": None,
            "seed_abundance": None,
            "conspicuous": None,
            "color": None
        },
        "foliage": {
            "texture": None,
            "porosity_winter": None,
            "porosity_summer": None,
            "color": None
        },
        "flower": {
            "conspicuous": None,
            "color": None
        },
        "family_common_name": "Aster family",
        "duration": "Annual, Perennial",
        "complete_data": False,
        "common_name": "common woolly sunflower",
        "bibliography": None,
        "author": None
    },
    "images": [
        {
            "url": "https://upload.wikimedia.org/wikipedia/commons"
                   "/b/b9/Eriophyllum_lanatum_3575.JPG"
        }
    ],
    "id": 134845,
    "hybrids": [],
    "genus": {
        "slug": "eriophyllum",
        "name": "Eriophyllum",
        "link": "http://trefle.io/api/genuses/494",
        "id": 494
    },
    "forms": [],
    "family_common_name": "Aster family",
    "family": None,
    "duration": "Annual, Perennial",
    "division": None,
    "cultivars": [],
    "common_name": "common woolly sunflower",
    "class": None
}

METEOSTAT_STATION_SEARCH_RESPONSE = {
    "meta": {},
    "data": [
        {
            "id": "03865",
            "name": "Southampton / Weather Centre",
            "distance": "7.4"
        },
        {
            "id": "03749",
            "name": "Middle Wallop",
            "distance": "11.5"
        },
        {
            "id": "03746",
            "name": "Boscombe Down",
            "distance": "16.5"
        },
        {
            "id": "03743",
            "name": "Larkhill",
            "distance": "19.6"
        },
        {
            "id": "03862",
            "name": "Bournemouth Airport",
            "distance": "20.4"
        },
        {
            "id": "03761",
            "name": "Odiham",
            "distance": "29.1"
        },
        {
            "id": "03866",
            "name": "Saint Catherine's Point",
            "distance": "29.3"
        },
        {
            "id": "03768",
            "name": "Farnborough",
            "distance": "37.6"
        },
        {
            "id": "03740",
            "name": "Lyneham",
            "distance": "41.1"
        },
        {
            "id": "03763",
            "name": "Bracknell / Beaufort Park",
            "distance": "41.2"
        }
    ]
}

METEOSTAT_STATION_WEATHER_RESPONSE = {
    "meta": {
        "source": "National Oceanic and Atmospheric Administration, Deutscher Wetterdienst"
    },
    "data": [
        {
            "month": "2019-01",
            "temperature_mean": 3.9,
            "temperature_mean_min": 1,
            "temperature_mean_max": 6.8,
            "temperature_min": -11.1,
            "temperature_max": 10.6,
            "precipitation": 97,
            "raindays": 13,
            "pressure": 1011,
            "sunshine": 66
        },
        {
            "month": "2019-02",
            "temperature_mean": 4.8,
            "temperature_mean_min": 1.5,
            "temperature_mean_max": 8.1,
            "temperature_min": -7.5,
            "temperature_max": 13.1,
            "precipitation": 89,
            "raindays": 8,
            "pressure": 1015.9,
            "sunshine": 64
        },
        {
            "month": "2019-03",
            "temperature_mean": 7,
            "temperature_mean_min": 1.7,
            "temperature_mean_max": 12.2,
            "temperature_min": -4.7,
            "temperature_max": 15.7,
            "precipitation": 44,
            "raindays": 7,
            "pressure": 1016.3,
            "sunshine": 166
        },
        {
            "month": "2019-04",
            "temperature_mean": 9.7,
            "temperature_mean_min": 5.1,
            "temperature_mean_max": 14.2,
            "temperature_min": -0.9,
            "temperature_max": 18.3,
            "precipitation": 50,
            "raindays": 9,
            "pressure": 1013.3,
            "sunshine": 175
        },
        {
            "month": "2019-05",
            "temperature_mean": 12.7,
            "temperature_mean_min": 7.7,
            "temperature_mean_max": 17.5,
            "temperature_min": 0.8,
            "temperature_max": 25.2,
            "precipitation": 26,
            "raindays": 6,
            "pressure": 1018.7,
            "sunshine": 217
        },
        {
            "month": "2019-06",
            "temperature_mean": 15.6,
            "temperature_mean_min": 10.1,
            "temperature_mean_max": 20.9,
            "temperature_min": 2.6,
            "temperature_max": 26.5,
            "precipitation": 61,
            "raindays": 7,
            "pressure": 1017.6,
            "sunshine": 231
        },
        {
            "month": "2019-07",
            "temperature_mean": 16.7,
            "temperature_mean_min": 12.9,
            "temperature_mean_max": 20.4,
            "temperature_min": 7.6,
            "temperature_max": 26.8,
            "precipitation": 75,
            "raindays": 16,
            "pressure": 1013.2,
            "sunshine": 187
        },
        {
            "month": "2019-08",
            "temperature_mean": 16.7,
            "temperature_mean_min": 12.4,
            "temperature_mean_max": 21,
            "temperature_min": 6.2,
            "temperature_max": 25.2,
            "precipitation": 29,
            "raindays": 8,
            "pressure": 1016.6,
            "sunshine": 181
        },
        {
            "month": "2019-09",
            "temperature_mean": 14.6,
            "temperature_mean_min": 9.4,
            "temperature_mean_max": 19.7,
            "temperature_min": 2.5,
            "temperature_max": 23.2,
            "precipitation": 41,
            "raindays": 5,
            "pressure": 1022.5,
            "sunshine": 171
        },
        {
            "month": "2019-10",
            "temperature_mean": 12.3,
            "temperature_mean_min": 8.4,
            "temperature_mean_max": 16.1,
            "temperature_min": -1,
            "temperature_max": 18.5,
            "precipitation": 79,
            "raindays": 13,
            "pressure": 1016.6,
            "sunshine": 92
        },
        {
            "month": "2019-11",
            "temperature_mean": 10,
            "temperature_mean_min": 7.1,
            "temperature_mean_max": 12.7,
            "temperature_min": 1,
            "temperature_max": 16.7,
            "precipitation": 109,
            "raindays": 22,
            "pressure": 1002.1,
            "sunshine": 69
        },
        {
            "month": "2019-12",
            "temperature_mean": 4.2,
            "temperature_mean_min": 1.1,
            "temperature_mean_max": 7.3,
            "temperature_min": -6.2,
            "temperature_max": 13,
            "precipitation": 53,
            "raindays": 9,
            "pressure": 1006.4,
            "sunshine": 74
        }
    ]
}
