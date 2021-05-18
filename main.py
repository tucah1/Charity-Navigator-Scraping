import lxml.html
from lxml import etree
from urllib import request as req
import pandas as pd

output_file = r'C:\Users\niX\Desktop\Work\charityscrape\charity_navigator_data.csv'
initial_url = 'https://www.charitynavigator.org/index.cfm?bay=search.alpha&ltr=1#ltr-1'

validity_test_xpath = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/span'
organization_name2 = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[2]/h1'
organization_name = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[1]/h1'
organization_score3 = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[6]/div[3]/div/div[1]/div/div[1]/table/tr/td/div/table/tr[2]/td[2]'
organization_score2 = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[5]/div[3]/div/div[1]/div/div[1]/table/tr/td/div/table/tr[2]/td[2]'
organization_score = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[4]/div[3]/div/div[1]/div/div[1]/table/tr/td/div/table/tr[2]/td[2]'
organization_rating2 = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[5]/div[3]/div/div[1]/div/div[1]/table/tr/td/div/table/tr[2]/td[3]/strong/svg/title'
organization_rating = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[4]/div[3]/div/div[1]/div/div[1]/table/tr/td/div/table/tr[2]/td[3]/strong/svg/title'
organization_mission3 = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[6]/div[3]/div/div[1]/div/div[3]/div[3]/div/div/p'
organization_mission2 = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[5]/div[3]/div/div[1]/div/div[3]/div[3]/div/div/p'
organization_mission = '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/div[4]/div[3]/div/div[1]/div/div[3]/div[3]/div/div/p'
organization_website2 = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div[1]/p[3]/a'
organization_website = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div[1]/p[2]/a'
organization_phone = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div[1]/p[1]'
organization_leadership = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div[2]/p[1]'
organization_ceo2 = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div[2]/p'
organization_ceo = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div[2]/p[2]'

organizations_container = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/div'

alphabet_list = '/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div/p[1]'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
}

column_names = ['organization_name',
                'score',
                'rating',
                'mission',
                'website',
                'phone',
                'fax',
                'leadership_name',
                'leadership_title',
                'ceo_name',
                'ceo_title']


def find_between(s, first, last):
    return s.split(first)[1].split(last)[0]


def get_html(page_url):
    http_request = req.Request(page_url,
                               headers=headers)
    response = req.urlopen(http_request)
    html = response.read()
    return html


def get_nav_list(page_html):
    tree = lxml.html.fromstring(page_html)
    nav_list_elem = tree.xpath(alphabet_list)[0]
    nav_list = []
    for x in nav_list_elem:
        if x.tag == 'a':
            nav_list.append(x.get('href'))

    return nav_list


def get_org_list(nav_list):
    org_list = []
    for url in nav_list:
        html = get_html(url)
        tree = lxml.html.fromstring(html)
        container = tree.xpath(organizations_container)
        org_list_temp = []
        for x in container[0]:
            if x.tag == 'a' and x.get('href') != '' and x.get('href'):
                org_list_temp.append(x.get('href'))

        org_list.append(org_list_temp)

    return org_list


def test_org_validity(xml_tree):
    elem = xml_tree.xpath(validity_test_xpath)
    if elem:
        return False
    else:
        return True


def scrape_single_org(xml_tree):
    title = ''
    rating = ''
    score = 0
    mission = ''
    website = ''
    ceo_name = ''
    ceo_title = ''
    leadership_name = ''
    leadership_title = ''
    phone = ''
    fax = ''
    try:
        title_elem = xml_tree.xpath(organization_name)
        if len(title_elem) == 0:
            title_elem = xml_tree.xpath(organization_name2)
        title_elem = title_elem[0]
        score_elem = xml_tree.xpath(organization_score)
        if len(score_elem) == 0:
            score_elem = xml_tree.xpath(organization_score2)
        if len(score_elem) == 0:
            score_elem = xml_tree.xpath(organization_score3)
        if len(score_elem) != 0:
            score_elem = score_elem[0]
            score = score_elem.text.strip()
        rating_elem = xml_tree.xpath(organization_rating)
        if len(rating_elem) == 0:
            rating_elem = xml_tree.xpath(organization_rating2)
        if len(rating_elem) == 0:
            rating_elem = 0
        else:
            rating_elem = rating_elem[0]
            if rating_elem.text.strip() == 'one star':
                rating = 1
            elif rating_elem.text.strip() == 'two stars':
                rating = 2
            elif rating_elem.text.strip() == 'three stars':
                rating = 3
            elif rating_elem.text.strip() == 'four stars':
                rating = 4
        mission_elem = xml_tree.xpath(organization_mission)
        if len(mission_elem) == 0:
            mission_elem = xml_tree.xpath(organization_mission2)
        if len(mission_elem) == 0:
            mission_elem = xml_tree.xpath(organization_mission3)
        if len(mission_elem) != 0:
            mission_elem = mission_elem[0]
            mission = mission_elem.text_content().strip().replace('&amp;', '&')

        website_elem = xml_tree.xpath(organization_website)
        if len(website_elem) == 0:
            website_elem = xml_tree.xpath(organization_website2)
        if len(website_elem) != 0:
            website = website_elem[0].get('href').strip()

        phone_elem = xml_tree.xpath(organization_phone)[0]

        title_test = xml_tree.xpath('/html/body/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div[2]/h1')
        if len(xml_tree.xpath(organization_ceo)) != 0:
            leadership_elem = etree.tostring(xml_tree.xpath(organization_leadership)[0]).decode('utf-8')
            ceo_elem = xml_tree.xpath(organization_ceo)[0]
            ceo_list = list(filter(lambda x: x != '',
                                   map(lambda x: x.strip(), ceo_elem.text_content().split('\n'))))
            ceo_name = ceo_list[0].replace('&amp;', '&')
            ceo_title = ceo_list[1].replace('&amp;', '&')
            leadership_name = find_between(leadership_elem, '<strong>', '</strong>').replace('&amp;', '&')
            leadership_title = find_between(leadership_elem, '<br/>', '<').replace('&amp;', '&')
        elif len(title_test) != 0 and title_test[0].text.strip() == 'Board Leadership':
            leadership_elem = etree.tostring(xml_tree.xpath(organization_leadership)[0]).decode('utf-8')
            leadership_name = find_between(leadership_elem, '<strong>', '</strong>').replace('&amp;', '&')
            leadership_title = find_between(leadership_elem, '<br/>', '<').replace('&amp;', '&')
        elif len(xml_tree.xpath(organization_ceo2)) != 0:
            ceo_elem = xml_tree.xpath(organization_ceo2)[0]
            ceo_list = list(filter(lambda x: x != '',
                                   map(lambda x: x.strip(), ceo_elem.text_content().split('\n'))))
            ceo_name = ceo_list[0].replace('&amp;', '&')
            ceo_title = ceo_list[1].replace('&amp;', '&')

        title = title_elem.text.strip().replace('&amp;', '&')

        if 'tel' in phone_elem.text_content():
            phone_list = \
            list(filter(lambda x: x[0:3] == 'tel', map(lambda x: x.strip(), phone_elem.text_content().split('\n'))))[
                0].split(' ')
            if len(phone_list) > 3:
                phone = phone_list[1] + ' ' + phone_list[2]
                fax = phone_list[4] + ' ' + phone_list[5]
            else:
                phone = phone_list[1] + ' ' + phone_list[2]

        row = dict(zip(
            column_names,
            [title, score, rating, mission, website, phone, fax, leadership_name, leadership_title, ceo_name, ceo_title]
        ))
        print(row)
        return row
    except:
        row = dict(zip(
            column_names,
            [title, score, rating, mission, website, phone, fax, leadership_name, leadership_title, ceo_name, ceo_title]
        ))
        print(row)
        return row


def scrape_nav_list(nav_list):
    org_list = get_org_list(nav_list)
    df = pd.DataFrame(columns=column_names)
    for group in org_list:
        for url in group:
            html = get_html(url)
            tree = lxml.html.fromstring(html)
            if test_org_validity(tree):
                df = df.append(scrape_single_org(tree), ignore_index=True)

    return df



def scrape_data():
    html = get_html(initial_url)
    nav_list = get_nav_list(html)
    df = scrape_nav_list(nav_list)
    print(df)
    df.to_csv(output_file)


if __name__ == '__main__':
    scrape_data()

