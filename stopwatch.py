#!/usr/bin/env python
# stopwatch is a pygame based stopwatch
# Copyright (C) 2011 Alejandro Varas
# based on code taken from http://www.bonf.net/2007/05/18/so/

######################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

import datetime

import pygame
import pygame.font
from pygame.colordict import THECOLORS


def main():
    fullscreen = True
    video_flags = fullscreen and pygame.FULLSCREEN
    pygame.init()

    # get the highest resolution
    resolution = pygame.display.list_modes()[0]

    # create our main window SDL surface
    surface = pygame.display.set_mode(resolution, video_flags)

    # get highest font size that fits resolution width
    font_size = int(resolution[1] / 1.2)
    font_size_fits = False
    max_string_length = resolution[0] / 8 * 7

    while not font_size_fits:
        font = pygame.font.SysFont('courier new', font_size)
        font_rect = font.size("00:00:00,00")
        if font_rect[0] > max_string_length:
            font_size = font_size - 10
        else:
            font_size_fits = True

    # get the point to draw the font in the midle of the screen
    font_blit_point = resolution[0] / 16, resolution[1] / 2 - font_rect[1] / 2

    on = False  # wheter the stopwatch is running or not
    milliseconds = 0  # milliseconds from start
    start_tick = 0  # the number of ticks when we began counting

    while True:
        event = pygame.event.poll()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                break

            if event.key == pygame.K_SPACE:
                if not on:
                    # starting the timer, so set the tick count reference to
                    # the current tick count plus the last tick count
                    start_tick = pygame.time.get_ticks() - milliseconds

                # swap value
                on = not on

            elif event.key == pygame.K_r:
                # initialize the tick count
                milliseconds = 0
                on = False

            elif event.key == pygame.K_f:
                # swap video mode widowed, fullscreen
                fullscreen = not fullscreen
                video_flags = (
                    fullscreen and pygame.FULLSCREEN) | (
                        not fullscreen and pygame.RESIZABLE)
                pygame.display.set_mode(resolution, video_flags)

        if on:
            milliseconds = (pygame.time.get_ticks() - start_tick)

        # render the time, by converting ticks to datetime.time + hundredth of
        # a second
        t = datetime.time(
            (milliseconds / 1000) / 3600, ((milliseconds / 1000) / 60 %
                                           60), (milliseconds / 1000) %
            60)
        h_o_s = str(milliseconds)[-3:][:2]  # hundredth of a second
        t_string = ','.join((t.strftime("%H:%M:%S"), h_o_s))
        tempsurface = font.render(t_string, 1, THECOLORS["black"])

        # fill the screen with white, to erase the previous time
        surface.fill(THECOLORS["white"])
        surface.blit(tempsurface, font_blit_point)

        pygame.display.flip()
        pygame.time.wait(1)


if __name__ == '__main__':
    main()