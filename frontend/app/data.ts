interface Thumbnail {
  url: string;
  width: number;
  height: number;
}

interface Item {
  id: string;
  title: string;
  artists: string[];
  album: string;
  duration: string;
  thumbnails: {
    default: Thumbnail;
    medium: Thumbnail;
    high: Thumbnail;
  };
  videoId: string;
  isExplicit: boolean;
  category: string;
  description: string;
}

export const items: Item[] = [
    {
      id: '1',
      title: 'Bohemian Rhapsody',
      artists: ['Queen'],
      album: 'A Night at the Opera',
      duration: '5:55',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/fJ9rUzIMcZQ/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/fJ9rUzIMcZQ/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/fJ9rUzIMcZQ/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'fJ9rUzIMcZQ',
      isExplicit: false,
      category: 'Classic Rock',
      description: 'A six-minute suite, notable for its lack of a refraining chorus and instead consisting of several sections',
    },
    {
      id: '2',
      title: 'Blinding Lights',
      artists: ['The Weeknd'],
      album: 'After Hours',
      duration: '3:20',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/4NRXx6U8ABQ/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/4NRXx6U8ABQ/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/4NRXx6U8ABQ/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: '4NRXx6U8ABQ',
      isExplicit: false,
      category: 'Pop',
      description: 'A synth-pop and nu-disco song with a pulsing beat and retro 1980s feel',
    },
    {
      id: '3',
      title: "Don't Start Now",
      artists: ['Dua Lipa'],
      album: 'Future Nostalgia',
      duration: '3:03',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/oygrmJFKYZY/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/oygrmJFKYZY/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/oygrmJFKYZY/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'oygrmJFKYZY',
      isExplicit: false,
      category: 'Pop',
      description: 'A disco-pop and nu-disco song with elements of 1970s disco and 1980s pop',
    },
    {
      id: '4',
      title: 'Watermelon Sugar',
      artists: ['Harry Styles'],
      album: 'Fine Line',
      duration: '2:54',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/E07s5ZYygMg/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/E07s5ZYygMg/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/E07s5ZYygMg/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'E07s5ZYygMg',
      isExplicit: false,
      category: 'Pop Rock',
      description: 'A pop rock and soft rock song with elements of funk and psychedelic pop',
    },
    {
      id: '5',
      title: 'Levitating',
      artists: ['Dua Lipa', 'DaBaby'],
      album: 'Future Nostalgia',
      duration: '3:23',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/TUVcZxfQlFY/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/TUVcZxfQlFY/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/TUVcZxfQlFY/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'TUVcZxfQlFY',
      isExplicit: false,
      category: 'Pop',
      description: 'A disco-pop and dance-pop song with elements of 1970s and 1980s dance music',
    },
    {
      id: '6',
      title: 'Save Your Tears',
      artists: ['The Weeknd'],
      album: 'After Hours',
      duration: '3:35',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/XXYlFuWEuKI/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/XXYlFuWEuKI/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/XXYlFuWEuKI/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'XXYlFuWEuKI',
      isExplicit: false,
      category: 'Pop',
      description: 'A synth-pop and new wave song with a retro 1980s feel',
    },
    {
      id: '7',
      title: 'Stay',
      artists: ['The Kid LAROI', 'Justin Bieber'],
      album: 'F*CK LOVE 3: OVER YOU',
      duration: '2:21',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/kTJczUoc26U/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/kTJczUoc26U/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/kTJczUoc26U/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'kTJczUoc26U',
      isExplicit: true,
      category: 'Pop',
      description: 'A pop and emo rap song with a melancholic yet catchy melody',
    },
    {
      id: '8',
      title: 'good 4 u',
      artists: ['Olivia Rodrigo'],
      album: 'SOUR',
      duration: '2:58',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/gNi_6U5Pm_o/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/gNi_6U5Pm_o/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/gNi_6U5Pm_o/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'gNi_6U5Pm_o',
      isExplicit: true,
      category: 'Pop Punk',
      description: 'A pop-punk and pop-rock song with angsty lyrics and a driving beat',
    },
    {
      id: '9',
      title: 'Montero',
      artists: ['Lil Nas X'],
      album: 'MONTERO',
      duration: '2:17',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/6swmTBVIpgk/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/6swmTBVIpgk/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/6swmTBVIpgk/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: '6swmTBVIpgk',
      isExplicit: true,
      category: 'Pop Rap',
      description: 'A pop-rap and trap song with a catchy melody and controversial themes',
    },
    {
      id: '10',
      title: 'Peaches',
      artists: ['Justin Bieber', 'Daniel Caesar', 'Giveon'],
      album: 'Justice',
      duration: '3:18',
      thumbnails: {
        default: { url: 'https://img.youtube.com/vi/tQ0yjYUFKae/default.jpg', width: 120, height: 90 },
        medium: { url: 'https://img.youtube.com/vi/tQ0yjYUFKae/mqdefault.jpg', width: 320, height: 180 },
        high: { url: 'https://img.youtube.com/vi/tQ0yjYUFKae/hqdefault.jpg', width: 480, height: 360 },
      },
      videoId: 'tQ0yjYUFKae',
      isExplicit: false,
      category: 'R&B',
      description: 'A smooth R&B track with melodic vocals and a laid-back vibe',
    },
  ];
  