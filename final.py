from final2 import get_info_from_link
from work import get_links_from_diff_pages

def get_info_final(links_base):
    return_master = []
    for link_base in links_base:
        for link in get_links_from_diff_pages(link_base):
            if not get_info_from_link(link_base):
                break
            return_master.append(get_info_from_link(link))
    return return_master
