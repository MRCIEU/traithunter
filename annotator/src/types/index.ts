export {};

declare global {
  interface Window {
    // turn off ts warning on attribute showOpenFilePicker
    showOpenFilePicker: any;
    showSaveFilePicker: any;
  }
}
