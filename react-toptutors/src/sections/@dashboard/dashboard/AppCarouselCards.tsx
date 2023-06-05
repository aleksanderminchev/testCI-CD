import { m } from 'framer-motion';
import { useState, useRef } from 'react';
// @mui
import { alpha, useTheme, styled } from '@mui/material/styles';
import { Card, Button, Typography, CardProps, Stack } from '@mui/material';
// utils
import { bgGradient } from '../../../utils/cssStyles';
// components
import Image from '../../../components/image';
import Carousel, { CarouselDots, CarouselArrows } from '../../../components/carousel';
import { MotionContainer, varFade } from '../../../components/animate';

// ----------------------------------------------------------------------

const StyledOverlay = styled('div')(({ theme }) => ({
  ...bgGradient({
    startColor: `${alpha(theme.palette.common.black, 0)} 0%`,
    endColor: `${theme.palette.common.black} 75%`,
  }),
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  zIndex: 8,
  position: 'absolute',
}));

// ----------------------------------------------------------------------

type ItemProps = {
  id: string;
  image: string;
  name: string;
  label: string;
  description: string;
};

interface Props extends CardProps {
  list: ItemProps[];
}

export default function AppCarouselCards({ list, ...other }: Props) {
  const theme = useTheme();

  const carouselRef = useRef<Carousel>(null);

  const [currentIndex, setCurrentIndex] = useState(theme.direction === 'rtl' ? list.length - 1 : 0);

  const carouselSettings = {
    speed: 1000,
    dots: true,
    arrows: false,
    autoplay: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    rtl: Boolean(theme.direction === 'rtl'),
    beforeChange: (current: number, next: number) => setCurrentIndex(next),
    ...CarouselDots({
      sx: {
        right: 20,
        bottom: 20,
        position: 'absolute',
      },
    }),
  };

  const handlePrev = () => {
    carouselRef.current?.slickPrev();
  };

  const handleNext = () => {
    carouselRef.current?.slickNext();
  };

  return (
    <Card {...other}>
      <Carousel ref={carouselRef} {...carouselSettings}>
        {list.map((item, index) => (
          <CarouselItem key={item.id} item={item} isActive={index === currentIndex} />
        ))}
      </Carousel>

      <CarouselArrows
        onNext={handleNext}
        onPrevious={handlePrev}
        sx={{ top: 8, right: 8, position: 'absolute', color: 'common.white' }}
      />
    </Card>
  );
}

// ----------------------------------------------------------------------

type CarouselItemProps = {
  item: ItemProps;
  isActive?: boolean;
};

function CarouselItem({ item, isActive }: CarouselItemProps) {
  const { image, name, label, description } = item;

  return (
    <MotionContainer action animate={isActive} sx={{ position: 'relative' }}>
      <Stack
        spacing={1}
        sx={{
          p: 3,
          width: 1,
          bottom: 0,
          zIndex: 9,
          textAlign: 'left',
          position: 'absolute',
          color: 'common.white',
        }}
      >
        <m.div variants={varFade().inRight}>
          <Typography variant="overline" sx={{ opacity: 0.48 }}>
            {label}
          </Typography>
        </m.div>

        <m.div variants={varFade().inRight}>
          <Typography noWrap variant="h5" sx={{ mt: 1, mb: 3 }}>
            {name}
          </Typography>
        </m.div>

        <m.div variants={varFade().inRight}>
          <Typography sx={{ mt: 1, mb: 3 }}>{description}</Typography>
        </m.div>

        <m.div variants={varFade().inRight}>
          <Button variant="contained">Læs mere</Button>
        </m.div>
      </Stack>

      <StyledOverlay />

      <Image
        alt={name}
        src={image}
        sx={{
          height: { xs: 280, xl: 320 },
        }}
      />
    </MotionContainer>
  );
}
