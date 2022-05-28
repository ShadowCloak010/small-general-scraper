import yaml
import asyncio
import os.path
import httpx
from httpx_socks import AsyncProxyTransport
import re
import lxml.etree
import elementpath

def getCfg():
    if (not os.path.isfile('cfg.yml')):
        raise FileNotFoundError('Not found the config file: cfg.yml')
    with open('cfg.yml', 'r') as F:
        cfg = yaml.load(F, yaml.SafeLoader)
        return cfg

    
async def getter(cli: httpx.AsyncClient, targets, totalArr):
    try:
        while (len(targets) > 0):
            target = targets.pop()
            url = target['url']
            patt = target['match']
            try:
                resp = await cli.get(url)
                if ( not resp.is_success ):
                    resp.raise_for_status()
                raw = resp.text
                mats = []
                if (target['type'] == 'regex'):
                    mats = re.findall(patt, raw, re.M)
                else:
                    root = lxml.etree.HTML(raw)
                    mats = elementpath.select(root, patt)
                totalArr.extend(mats)
                print('Got %d results\tfrom URL: %s' % (len(mats), url))

            except Exception as e:
                print('Occurred error when scraping from URL: %s\t%s' % (url, e))
                continue
    except Exception as e:
        print('Error occurred from worker: %s' % (e))
        

async def main():
    cli = None
    try:
        CFG = getCfg()
        if ( (not CFG['sources']) or len(CFG['sources']) == 0):
            print("Haven't any sources in config")
            return
        transport = AsyncProxyTransport.from_url(CFG['proxyUrl'])
        cli = httpx.AsyncClient(
            transport=transport,
            headers=CFG['headers']
        )
        workers = []
        total = []
        print('Starting scraper..')
        for i in range(CFG['maxWorkers']):
            workers.append(getter(cli, CFG['sources'], total))
        
        await asyncio.gather(*workers)
        totalDeduplication = list(set(total))
        print('All of works have finished, total results: %d (removed duplications)' % (len(totalDeduplication)))
        if (len(totalDeduplication) > 0):
            print('Writing results to file: %s ..' % (CFG['outputName']))
            with open(CFG['outputName'], 'w') as F:
                F.write('\n'.join(totalDeduplication))
        else:
            print("Haven't got any datas")
        print('Quitting..')
        
    except Exception as e:
        print('Internal error occurred：%s' % (e))
    finally:
        if (cli):
            await cli.aclose()
        

asyncio.run(main())