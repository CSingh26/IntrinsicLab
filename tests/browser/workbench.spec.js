import {test,expect} from '@playwright/test';

test('valuation controls, visual evidence, and saved cases survive reload', async({page})=>{
  await page.goto('/');
  await expect(page.locator('#mode')).toHaveText('DEMO DATA');
  await expect(page.locator('#summary strong').first()).toContainText('USD');
  await expect(page.locator('#forecast-chart svg')).toBeVisible();
  const original=await page.locator('#summary strong').first().textContent();
  await page.locator('[name="wacc"]').fill('12');
  await expect(page.locator('#summary')).toContainText('Recalculate');
  await page.locator('#calculate').click();
  await expect(page.locator('#summary strong').first()).not.toHaveText(original);
  await page.locator('#save-case').click();
  await page.reload();
  await expect(page.locator('#cases .case')).toHaveCount(1);
  await page.locator('[data-case="0"]').click();
  await expect(page.locator('[name="wacc"]')).toHaveValue('12');
});

test('invalid economics clear results and WACC calculator drives valuation', async({page})=>{
  await page.goto('/');await expect(page.locator('#summary strong').first()).toBeVisible();
  await page.locator('[name="terminal_growth"]').fill('10');await page.locator('#calculate').click();
  await expect(page.locator('#error')).toContainText('below WACC');
  await expect(page.locator('#summary strong')).toHaveCount(0);
  await page.locator('[data-tab="capital"]').click();
  await page.locator('#capital-form button').click();
  await expect(page.locator('#capital-result')).toContainText('WACC');
});

test('mobile screen retains usable controls without page overflow',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto('/');
  await expect(page.locator('#summary strong').first()).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
});
