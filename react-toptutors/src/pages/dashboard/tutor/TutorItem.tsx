import { useParams, useNavigate } from 'react-router-dom';
// @mui
import { styled } from '@mui/material/styles';
import { Box, Tooltip, Typography, Checkbox, Stack, TypographyProps } from '@mui/material';
// hooks
import useResponsive from '../../../hooks/useResponsive';
// utils
import { fDate } from '../../../utils/formatTime';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// @types
import { ITutor } from '../../../@types/tutor';
// components
import Label from '../../../components/label';

import Iconify from '../../../components/iconify';
//
type Props = {
  tutor: ITutor;
  selected: boolean;
};

export default function TutorItem({ tutor, selected, ...other }: Props) {
  const params = useParams();

  const navigate = useNavigate();

  const isDesktop = useResponsive('up', 'md');

  const handleClick = () => {
    // navigate(linkTo(params, tutor.id));
  };

  return <Typography>{tutor.email}</Typography>;
}

const linkTo = (
  params: {
    [key: string]: string | string[] | undefined;
  },
  tutorId: string
) => {
  const baseUrl = PATH_DASHBOARD.tutor.profile;

  return baseUrl;
};
