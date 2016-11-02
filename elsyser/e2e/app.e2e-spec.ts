import { ElsyserPage } from './app.po';

describe('elsyser App', function() {
  let page: ElsyserPage;

  beforeEach(() => {
    page = new ElsyserPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
