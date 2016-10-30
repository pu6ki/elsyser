import { ElsyserWebClientPage } from './app.po';

describe('elsyser-web-client App', function() {
  let page: ElsyserWebClientPage;

  beforeEach(() => {
    page = new ElsyserWebClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
