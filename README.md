# COVID-19

El crecimiento del número de casos relacionados con el reciente brote de COVID-19
en las provincias de China continental se puede modelar mediante un nuevo modelo de contención SIR.
Este trabajo esta basado en los datos proporcionados por [B. F. Maier y D. Brockmann, "La contención efectiva explica el crecimiento sub-exponencial en casos confirmados de brote reciente de COVID-19 en China continental", 2020] (https://arxiv.org/abs/2002.07572).

## Informacion 

El json- `data/all_confirmed_cases_with_population.json` 
contiene datos del número de caso de las provincias actualmente afectadas en China, así como el tamaño de la población.

La serie de tiempo cuenta el número total de personas cuya infección fue confirmada por laboratorio.
La informacion fue sacada del repositorio [Johns Hopkins University Center for Systems Science and Engineering](https://github.com/CSSEGISandData/COVID-19).

Desde el 12 de febrero, los datos de Hubei también incluyen casos sintomáticos sin confirmación de laboratorio,
por lo tanto, solo se ha considerado datos anteriores al 12 de febrero a las 6 a. m

## Pre requisitos

Python 3.7

### Requerimientos

```
simplejson==3.16.0
numpy==1.17.2
scipy==1.3.1
bfmplot==0.0.7
lmfit==0.9.12
tabulate==0.8.2
matplotlib==3.0.2
tqdm==4.28.1
```

## Ejemplos

Para reproducir los graficos del trabajo se deben ejecutar los distintos .py que figuran en el repositorio.
Se puede utilizar los datos que se proporcionan en la carpeta fit_parameters.
En el caso de que no se le pase ningun archivo como parametro, el programa genera un nuevo set de datos que sobreescribira el anterior.

Por ejemplo para el caso del modelo completo con cuarentena y contencion se deje ejecutar:

cd main_results
py modelo_completo_hubei_china_lineal.py fit_parameters/hubei_china.p
py modelo_completo_paises_mas_500_confirmados.py fit_parameters/confirmed_cases_500.p

para el ultimo caso, si se quiere generar un nuevo set de parametros, se debe ejecutar directamente
py modelo_completo_paises_mas_500_confirmados.py

y esos nuevos parametros se guardaran en `main/results/fit_parameters/confirmed_cases_500.p`

Los graficos generados se guardaran en

![modelFitHubeiMainland](main_results/model_fit_figures/hubei_y_china_modelo_completo_lineal.png)

![modelFitConfirmed500](main_results/model_fit_figures/modelo_completo_prov_500_casos.png)

Funciona de la misma manera para el resto de los modelos.
