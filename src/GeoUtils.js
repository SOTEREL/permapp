import axios from 'axios';
import * as Gp from '@ignf-geoportal/sdk-2d';

let _ignApiKey = null;

const getParcelShape = (inseeCode, section, number) => {
  return axios.get('https://apicarto.ign.fr/api/cadastre/parcelle', {
      params: {
        apikey: _ignApiKey,
        code_insee: inseeCode,
        section: section,
        numero: number,
      },
    })
    .then(resp => resp.data);
};

export const getParcelShapeFromPos = position => {
  return new Promise((resolve, reject) => {
    Gp.Services.reverseGeocode({
      apiKey: _ignApiKey,
      position: { x: position[0], y: position[1] },
      filterOptions: {
        type: ['CadastralParcel']
      },
      onSuccess: (resp) => {
        const parcel = resp.locations[0];
        if (parcel === undefined) {
          reject('No parcels found');
        }
        getParcelShape(
          parcel.placeAttributes.insee,
          parcel.placeAttributes.section,
          parcel.placeAttributes.number
        )
        .then(resolve)
        .catch(reject);
      },
      onFailure: reject,
    });
  });
};

export const setIGNApiKey = key => _ignApiKey = key;
