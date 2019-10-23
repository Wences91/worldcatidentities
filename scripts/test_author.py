from worldcatidentities import Authority, AuthorityData

author = Authority('Federico Gracía Lorca')
author.search()
author.fixed_name

author = AuthorityData('Federico Gracía Lorca')
author.data()
author.works
author.name

for i in ['Federico Gracía Lorca', 'Virginia Woolf']:
    authority = AuthorityData(i).data()
    print(authority.name)
    print(authority.works)