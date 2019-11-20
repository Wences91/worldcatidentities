from worldcatidentities import Authority, AuthorityData

author = Authority('Federico Gracía Lorca')
author.search()
author.fixed_name

author = AuthorityData(name = 'Federico Gracía Lorca')
author.data()
author.works
author.name

author = AuthorityData(uri = 'lccn-n79034425')
author.data()
author.works
author.name

for i in ['Federico Gracía Lorca', 'Virginia Woolf']:
    authority = AuthorityData(name = i).data()
    print(authority.name)
    print(authority.works)