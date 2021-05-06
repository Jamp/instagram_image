from instagram_image import get_image, get_avatar

if __name__ == '__main__':
    test_image = 'https://instagram.flim1-2.fna.fbcdn.net/v/t51.2885-15/e35/182368529_211027277228393_6964653241994119240_n.jpg?tp=1&_nc_ht=instagram.flim1-2.fna.fbcdn.net&_nc_cat=1&_nc_ohc=iRxP2P3J-pQAX8SyFti&edm=AIQHJ4wBAAAA&ccb=7-4&oh=9c2e31f2fdf1c163d2f275b60a68c03f&oe=60B8B150&_nc_sid=7b02f1'
    test_avatar = 'https://instagram.flim1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/181542794_284132116756487_6091007168826666593_n.jpg?tp=1&_nc_ht=instagram.flim1-2.fna.fbcdn.net&_nc_ohc=US5G5u9cP4IAX97zxeo&edm=AEF8tYYBAAAA&ccb=7-4&oh=2e1d5ea9cd6990cf74863fbf07e7e0c1&oe=60BAA490&_nc_sid=a9513d'

    image = get_image(test_image, '123')
    avatar = get_avatar(test_avatar, '321')

    print(image)
    print(avatar)
