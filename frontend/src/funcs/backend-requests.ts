import _ from "lodash";
import axios from "axios";

import store from "@/store/index";
import { web_backend_url } from "@/config";
import * as types from "@/types/types";

function snackbarError(message: string | null = null): void {
  const generalWarningMessage = `
    Error occurred when requesting data.
    Please adjust your query settings.
  `;
  const warningMessage = message ? message : generalWarningMessage;
  store.commit("snackbar/showSnackbar", { text: warningMessage });
}

export async function getPing(): Promise<boolean> {
  const url = `${web_backend_url}/ping`;
  const response = (await axios
    .get(url)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
      });
      snackbarError();
    })) as unknown;
  const res = response as boolean;
  return res;
}

export async function getDictionaryOptions(): Promise<string[]> {
  const url = `${web_backend_url}/entity/dictionary/list`;
  const response = (await axios
    .get(url)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
      });
      snackbarError();
    })) as unknown;
  const res = response as string[];
  return res;
}

export async function getEntityOptions(
  q: string,
  dictionary: string,
): Promise<types.BaseEnt[]> {
  const url = `${web_backend_url}/entity/info/search`;
  const params = {
    q: q,
    dictionary: dictionary,
  };
  const response = (await axios
    .get(url, { params: params })
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
      });
      snackbarError();
    })) as unknown;
  const res = _.chain(response)
    .map((e) => ({
      ent_id: e.id,
      ent_term: e.label,
      dictionary: dictionary,
    }))
    .value() as types.BaseEnt[];
  return res;
}
