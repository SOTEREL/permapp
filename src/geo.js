import axios from 'axios';
import Gp from 'geoportal-access-lib';

import Config from './config';

const getParcelShape = (inseeCode, section, number) =>
  axios.get('https://apicarto.ign.fr/api/cadastre/parcelle', {
    params: {
      apikey: Config.apiKeys.ign,
      code_insee: inseeCode,
      section: section,
      numero: number,
    },
  })
  .then(resp => resp.data);

export const getParcelShapeFromPos = position => new Promise((resolve, reject) => {
  Gp.Services.reverseGeocode({
    apiKey: Config.apiKeys.ign,
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
